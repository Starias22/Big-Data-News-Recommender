import json
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, regexp_replace, trim, concat_ws, udf,from_json
from pyspark.sql.types import StructType, StructField, StringType,DoubleType, ArrayType,IntegerType
from pyspark.ml.feature import StopWordsRemover, Tokenizer
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import download, WordNetLemmatizer
from pyspark.ml import PipelineModel





class NewsProcessor:
    def __init__(self, lemmatizer_broadcast):
        #self.lemmatizer = WordNetLemmatizer()
        self.sia = SentimentIntensityAnalyzer()       
        self.lda_pipeline = PipelineModel.load('../models/news_topic_model')  # Make sure this path is correct
    def clean(self, raw_articles):
        articles = raw_articles.na.drop(subset=['url', 'content', 'description'])
        articles = articles.withColumn("description_cleaned",
                           trim(
                               regexp_replace(
                                   regexp_replace(col("description"), r'[^a-zA-Z0-9\s]', ''),
                                   r'\s+', ' ')
                               )
                           )
        articles = articles.withColumn("description_cleaned", lower(col("description_cleaned")))
        return articles

    def tokenize(self, cleaned_articles):

        tokenizer = Tokenizer(inputCol="description_cleaned", outputCol="words")

        return tokenizer.transform(cleaned_articles)


    def lemmatize(self,tokenized_articles):
        # Apply the lemmatization UDF
        df_lemmatized =tokenized_articles.withColumn("lemmas", lemmatize_udf(col("words")))
        return df_lemmatized
    
    def stopwords_removal(self, lemmatized_articles):
        remover = StopWordsRemover(inputCol="lemmas", outputCol="description_filtered")
        return remover.transform(lemmatized_articles)

    def transform(self, articles, to_str=True):

        tokenized_data = self.tokenize(articles)
        lemmatized_data = self.lemmatize(tokenized_data)
        filtered_data = self.stopwords_removal(lemmatized_data)
        if to_str:
            filtered_data = filtered_data.withColumn("description_filtered_str", concat_ws(" ", "description_filtered"))
        return filtered_data

    def preprocess(self, articles, to_str=True):
        cleaned_data = self.clean(articles)
        
        transformed_data = self.transform(cleaned_data, to_str=to_str)

        return transformed_data

    
download('wordnet')
download('vader_lexicon')
download('punkt')
download('stopwords')

    
def get_sentiment_score(text):
    sia = SentimentIntensityAnalyzer()
    if text:
        return sia.polarity_scores(text)['compound']
    else:
        return None


with open('../config/config.json', 'r') as config_file:
    config = json.load(config_file)

# Initialize Spark Session with Kafka package
spark = SparkSession.builder \
    .appName("NewsStreamProcessor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .getOrCreate()


lemmatizer = WordNetLemmatizer()

# Broadcast the lemmatizer to all workers
lemmatizer_broadcast = spark.sparkContext.broadcast(lemmatizer)
def lemmatize_tokens(tokens):
        lemmatizer = lemmatizer_broadcast.value
        return [lemmatizer.lemmatize(token) for token in tokens]
lemmatize_udf = udf(lemmatize_tokens, ArrayType(StringType()))


# Define the schema for the JSON data
schema = StructType([
    StructField("title", StringType(), True),
    StructField("description", StringType(), True),
    StructField("content", StringType(), True),

    StructField("source_id", StringType(), True),
    StructField("source_name", StringType(), True),
    StructField("url", StringType(), True),
    StructField("img_url", StringType(), True),
    StructField("publication_date", StringType(), True),
    StructField("lang", StringType(), True),
])

# Read the data from the Kafka topic
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", config['kafka_bootstrap_servers']) \
    .option("subscribe", config["raw_news_topic"]) \
    .load()

# Deserialize the JSON data
news_df = kafka_df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

# Process the data (e.g., print it to the console)
query = news_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Initialize NewsProcessor
news_processor = NewsProcessor(lemmatizer_broadcast=lemmatizer_broadcast)
# Preprocess the data

preprocessed_news_df = news_processor.preprocess(news_df)
print('******************************')


sentiment_udf = udf(get_sentiment_score, DoubleType())


# Apply sentiment analysis directly
news_with_sentiment_df = preprocessed_news_df.withColumn("sentiment_score", sentiment_udf(preprocessed_news_df["description_filtered_str"]))

# Get topic distribution
def get_topic_distribution(preprocessed_data):
    topics_distribution = news_processor.lda_pipeline.transform(preprocessed_data)
    max_index_udf = udf(lambda topicDistribution: int(np.argmax(topicDistribution)), IntegerType())
    return topics_distribution.withColumn("most_dominant_topic", max_index_udf(topics_distribution.topicDistribution))

sentimenst_with_topics_df=get_topic_distribution(news_with_sentiment_df)
print('*********************************************')

query = sentimenst_with_topics_df.select(['description','sentiment_score','topicDistribution']) \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
