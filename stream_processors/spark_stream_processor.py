from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType
import json

# Load the configuration from the JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Initialize Spark Session with Kafka package
spark = SparkSession.builder \
    .appName("NewsProcessor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .getOrCreate()

# Define the schema for the JSON data
schema = StructType([
    StructField("title", StringType(), True),
    StructField("description", StringType(), True),
    StructField("source_id", StringType(), True),
    StructField("source_name", StringType(), True),
    StructField("url", StringType(), True),
    StructField("img_url", StringType(), True),
    StructField("publication_date", StringType(), True),
    StructField("lang", StringType(), True)
])

# Read the data from the Kafka topic
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", config['kafka_bootstrap_servers']) \
    .option("subscribe", config["news_topic"]) \
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

query.awaitTermination()
