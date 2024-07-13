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
    StructField("category", StringType(), True),
    #StructField("description_filtered_str", StringType(), True),

])
print('****************')

# Initialize Spark Session with Kafka package
spark = SparkSession.builder \
    .appName("ProcessedNewsForwardingApp") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .getOrCreate()

def forward_news():
    
    
    # Read data from Kafka topic
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", PROCESSED_NEWS_TOPIC) \
        .option("startingOffsets", "earliest") \
        .load()   
     
    # Deserialize JSON data
    news_df = kafka_df.selectExpr("CAST(value AS STRING) as json") \
        .select(from_json(col("json"), processed_news_schema).alias("data")) \
        .select("data.*")
    
    news_df=news_df.selectExpr("to_json(struct(*)) AS value")
    
    # Write stream to Kafka
    recommended_news_query = news_df.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("topic", AVAILABLE_NEWS_TOPIC) \
        .option("checkpointLocation", AVAILABLE_NEWS_CHECKPOINT_DIR) \
        .trigger(once=True) \
        .start()
    
    recommended_news_query.awaitTermination()

if __name__ == "__main__":
    forward_news()
