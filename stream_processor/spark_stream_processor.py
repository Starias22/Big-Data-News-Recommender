import json
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, ArrayType, IntegerType
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import WordNetLemmatizer
from news_preprocessor import NewsPreprocessor

# Load category mapping and config
with open('../models/news_categorization_model/new_categories.json') as f:
    category_mapping = json.load(f)
with open('../config/config.json', 'r') as config_file:
    config = json.load(config_file)

# Convert keys to integers for category mapping
category_mapping = {int(k): v for k, v in category_mapping.items()}

# Initialize Spark Session with Kafka package
spark = SparkSession.builder \
    .appName("NewsStreamProcessor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .getOrCreate()

# Function to get sentiment score using VADER
def get_sentiment_score(text):
    sia = SentimentIntensityAnalyzer()
    if text:
        return sia.polarity_scores(text)['compound']
    else:
        return None

# Initialize and broadcast lemmatizer
lemmatizer = WordNetLemmatizer()
lemmatizer_broadcast = spark.sparkContext.broadcast(lemmatizer)

# Lemmatization UDF
def lemmatize_tokens(tokens):
    lemmatizer = lemmatizer_broadcast.value
    return [lemmatizer.lemmatize(token) for token in tokens]
lemmatize_udf = udf(lemmatize_tokens, ArrayType(StringType()))

# Function to categorize news articles
def categorize_news(news):
    return news_processor.categorization_pipeline.transform(news)

# Function to get topic distribution
def get_topic_distribution(preprocessed_data):
    topics_distribution = news_processor.lda_model.transform(preprocessed_data)
    max_index_udf = udf(lambda topicDistribution: int(np.argmax(topicDistribution)), IntegerType())
    return topics_distribution.withColumn("most_dominant_topic", max_index_udf(topics_distribution.topicDistribution))

# UDF to map prediction to category
def map_prediction_to_category(prediction):
    return category_mapping.get(int(prediction), "Unknown")
map_prediction_to_category_udf = udf(map_prediction_to_category, StringType())



# Read data from Kafka topic
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", config['kafka_bootstrap_servers']) \
    .option("subscribe", config["raw_news_topic"]) \
    .load()

# Initialize NewsPreprocessor
news_processor = NewsPreprocessor(lemmatize_udf)

# Deserialize JSON data
news_df = kafka_df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), news_processor.schema).alias("data")) \
    .select("data.*")



# Preprocess the data
preprocessed_news_df = news_processor.preprocess(news_df)

# UDF for sentiment analysis
sentiment_udf = udf(get_sentiment_score, DoubleType())

# Apply sentiment analysis
df = preprocessed_news_df.withColumn("sentiment_score", sentiment_udf(preprocessed_news_df["description_filtered_str"]))

# Get topic distribution and drop unnecessary columns
df1 = get_topic_distribution(df)
df1 = df1.drop('rawFeatures').drop('features')

# Categorize news articles
df2 = categorize_news(df1)
df3 = df2.withColumn("category", map_prediction_to_category_udf(df2["prediction"]))

# Write stream to console
query = df3.select(['publication_date','description', 'sentiment_score', 'most_dominant_topic', 'category', 'prediction']) \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .trigger(processingTime="40 seconds") \
    .option("truncate", "false") \
    .option("numRows", 30) \
    .start()

# Await termination of the query
query.awaitTermination()
