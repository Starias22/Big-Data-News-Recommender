import json
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, from_json, when
from pyspark.sql.types import StringType, DoubleType, ArrayType, IntegerType, StructField, StructType
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import WordNetLemmatizer,download,data
from pathlib import Path
import sys
#curl -O <https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.13/3.3.0/spark-sql-kafka-0-10_2.13-3.3.0.jar>
#org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1
#curl -O <https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.1/spark-sql-kafka-0-10_2.12-3.5.1.jar>

POLL_TIMEOUT_MS = 5000  # 30 seconds poll timeout
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))
#print(src_path)
from news_preprocessor import NewsPreprocessor
from config.config import KAFKA_BOOTSTRAP_SERVERS,RAW_NEWS_TOPIC,FILTERED_NEWS_TOPIC,PROCESSED_NEWS_TOPIC,CATEGORIES_JSON_PATH,FILTERED_NEWS_CHECKPOINT_DIR,PROCESSED_NEWS_CHECKPOINT_DIR,NLTK_DATA_PATH

#from config.config import CATEGORIES_JSON_PATH

from nltk.corpus import wordnet



print('Downloaded****')

schema = StructType([
    StructField("size", IntegerType(), False),
    StructField("indices", ArrayType(IntegerType()), False),
    StructField("values", ArrayType(DoubleType()), False)
])

# Load category mapping and config
with open(CATEGORIES_JSON_PATH, 'r') as f:
    category_mapping = json.load(f)

# Convert keys to integers for category mapping
category_mapping = {int(k): v for k, v in category_mapping.items()}

# Initialize Spark Session with Kafka package
spark = SparkSession.builder \
    .appName("RawNewsStreamProcessingApp") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
        .getOrCreate()

# Function to get sentiment score using VADER
def get_sentiment_score(text):
    data.path=[NLTK_DATA_PATH]
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
    data.path=[NLTK_DATA_PATH]
   
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

# Initialize NewsPreprocessor
news_processor = NewsPreprocessor(lemmatize_udf)

def process_raw_news_stream():
    
    
    print('***************************')
    
    # Read data from Kafka topic
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", RAW_NEWS_TOPIC) \
        .option("startingOffsets", "earliest") \
        .option("failOnDataLoss", "false") \
        .load()
#.option("failOnDataLoss", "false") \
#.option("kafka.consumer.poll.timeout.ms", POLL_TIMEOUT_MS) \
#.option("startingOffsets", "earliest") \
    # Deserialize JSON data
    news_df = kafka_df.selectExpr("CAST(value AS STRING) as json") \
        .select(from_json(col("json"), news_processor.schema).alias("data")) \
        .select("data.*")

    # Filter the news articles to remove duplicates and news without URL, content or description
    filtered_news_df = news_processor.filter(news_df)

    raw_news_df = filtered_news_df.select(['id', 'title', 'description','author',
                                           'source_name', 'url', 'img_url',
                                           'publication_date', 'lang']).selectExpr("to_json(struct(*)) AS value")

    # Save the filtered news DataFrame to a temporary location as a stream
    filtered_news_query = raw_news_df.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("topic", FILTERED_NEWS_TOPIC) \
        .option("checkpointLocation", FILTERED_NEWS_CHECKPOINT_DIR) \
        .trigger(once=True)\
        .option("failOnDataLoss", "false") \
        .start()

    # Preprocess the filtered news
    preprocessed_news_df = news_processor.preprocess(filtered_news_df)

    # UDF for sentiment analysis
    sentiment_udf = udf(get_sentiment_score, DoubleType())

    # Apply sentiment analysis
    df = preprocessed_news_df.withColumn("sentiment_score", sentiment_udf(preprocessed_news_df["description_filtered_str"]))

    # Categorize news articles
    df = categorize_news(df)

    print('We are here')
    df = df.withColumn("category", map_prediction_to_category_udf(df["prediction"]))
    df = df.withColumn("sentiment_label", 
                    when(col("sentiment_score") == 0, 0)
                    .when(col("sentiment_score") > 0, 1)
                    .otherwise(-1))
    df = df.select(["id", "sentiment_label", "title", "features", "description", "publication_date",
                    "source_name", "author", "url", "img_url", "lang",
                    "sentiment_score", "prediction", "category",
                    ])

    # Define UDF to transform 'features' column
    #
    # Select and convert the entire dataframe to JSON
    processed_news_json_df = df.selectExpr("to_json(struct(*)) AS value")

    print('News processed successfully')
    print('Sending the news messages to Kafka')
    # Function to process each batch
    
#.foreachBatch(process_batch) \
    # Write the processed data to a Kafka topic
    query = processed_news_json_df.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("topic", PROCESSED_NEWS_TOPIC) \
        .option("checkpointLocation", PROCESSED_NEWS_CHECKPOINT_DIR) \
        .trigger(once=True)\
        .start()
    
    
#.option("checkpointLocation", f"{SPARK_STREAM_CHECKPOINT_LOCATION}/processed_news") \

    # Await termination of the query
    filtered_news_query.awaitTermination()
    import time
    print('We are here')
    #print(query.status)
    #time.sleep(60)
    #print(query.status)
    #query.stop()
    query.awaitTermination()
    print('Streaming terminated')

    
    spark.stop()
    print('Spark application stopped')

if __name__ == "__main__":
    process_raw_news_stream()
