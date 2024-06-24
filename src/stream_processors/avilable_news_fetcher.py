from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_json, struct
from pyspark.sql.types import StringType, IntegerType, StructField, StructType,ArrayType,DoubleType
from pathlib import Path
import sys

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))

# Import configurations
from config.config import KAFKA_BOOTSTRAP_SERVERS, PROCESSED_NEWS_TOPIC, AVAILABLE_NEWS_TOPIC, AVAILABLE_NEWS_CHECKPOINT_DIR

# Define schema for the features column
features_schema = StructType([
    StructField("type", IntegerType(), True),
    StructField("size", IntegerType(), True),
    StructField("indices", ArrayType(IntegerType()), True),
    StructField("values", ArrayType(DoubleType()), True)
])

# Define schema for the processed news
processed_news_schema = StructType([
    StructField("id", StringType(), True),
    StructField("title", StringType(), True),
    StructField("description", StringType(), True),
    StructField("source_name", StringType(), True),
    StructField("url", StringType(), True),
    StructField("img_url", StringType(), True),
    StructField("publication_date", IntegerType(), True),
    StructField("lang", StringType(), True),
    StructField("author", StringType(), True),
    StructField("prediction", DoubleType(), True),
    StructField("sentiment_label", IntegerType(), True),
    StructField("sentiment_score", DoubleType(), True),
    StructField("features", features_schema, True),

])

# Initialize Spark Session with Kafka package
spark = SparkSession.builder \
    .appName("ProcessedNewsFetcher") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .getOrCreate()

def process_raw_news_stream():
    servers_str = ",".join(KAFKA_BOOTSTRAP_SERVERS)
    
    # Read data from Kafka topic
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", servers_str) \
        .option("subscribe", PROCESSED_NEWS_TOPIC) \
        .option("startingOffsets", "earliest") \
        .load()
    
    # Print schema of incoming data for debugging
    kafka_df.printSchema()
    
    # Deserialize JSON data
    news_df = kafka_df.selectExpr("CAST(value AS STRING) as json") \
        .select(from_json(col("json"), processed_news_schema).alias("data")) \
        .select("data.*")
    
    news_df=news_df.selectExpr("to_json(struct(*)) AS value")
    # Print schema of deserialized data for debugging
    #news_df.printSchema()

    # Convert DataFrame to JSON and add value column
    #news_with_value_df = news_df.withColumn("value", to_json(struct([news_df[x] for x in news_df.columns])))

    # Write stream to Kafka
    recommended_news_query = news_df.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", servers_str) \
        .option("topic", anext) \
        .option("checkpointLocation", AVAILABLE_NEWS_CHECKPOINT_DIR) \
        .trigger(once=True) \
        .start()
    
    recommended_news_query.awaitTermination()

if __name__ == "__main__":
    process_raw_news_stream()
