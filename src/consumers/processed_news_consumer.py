import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType, StructType, StructField, IntegerType,DoubleType, StringType, DoubleType, ArrayType, MapType
from pymongo import MongoClient
from similarity import look_for_similarity
from pathlib import Path
import sys

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[1]
sys.path.append(str(src_path))
from db.interaction_db import InteractionDB


# Assuming you have defined your User class and user database access in src.db.user_db
from db.user_db import UserDB

# Load configuration
with open('../../config/config.json', 'r') as config_file:
    config = json.load(config_file)

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("ProcessedNewsConsumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .getOrCreate()

# Define schema for the features column
features_schema = StructType([
    StructField("type", IntegerType(), True),
    StructField("size", IntegerType(), True),
    StructField("indices", ArrayType(IntegerType()), True),
    StructField("values", ArrayType(DoubleType()), True)
])

# Define schema for the Kafka message value
schema = StructType([
    StructField("id", StringType(), True),
    StructField("title", StringType(), True),
    StructField("description", StringType(), True),
    #StructField("content", StringType(), True),
    StructField("source_id", StringType(), True),
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
interaction_db=InteractionDB()

def get_seen_and_liked_news(seen_news):
    news_ids = []
    for news in seen_news:
        for news_id, value in news.items():
            if value == 0 or value == 1:
                news_ids.append(news_id)
    return news_ids

# Read data from Kafka topic
kafka_df = spark.read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", config['kafka_bootstrap_servers']) \
    .option("subscribe", config["processed_news_topic"]) \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()

# Deserialize JSON data
processed_news_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")


# Sort the DataFrame in descending order based on publication_date
processed_news_df = processed_news_df.orderBy(col("publication_date").desc())
print('The processed news df is:')

processed_news_df.show()
# Initialize MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client["news_recommendation_db"]
user_preferences_collection = db["users"]

# Retrieve user preferences using UserDB class
user_db = UserDB()
users = user_db.retrieve_user_preferences()

# Process each user and update recommended_news
for user in users:
    user_id = user.id
    categories = user.categories
    sentiments = user.sentiments
    ansa=user.ansa
    seen_and_liked_news_ids = get_seen_and_liked_news(user.seen_news)
     # Retrieve filtered interactions
    filtered_interactions = interaction_db.retrieve_all_interactions(seen_and_liked_news_ids)
    filtered_interactions=[interaction.to_dict()['features'] for interaction in filtered_interactions]

    print('The user id is:', user_id)
    print('The email of the user is:', user.email)
    print('The sentiments are:', sentiments)
    print('Seen and liked news IDs:', seen_and_liked_news_ids)

    print('Filtered interactions:',filtered_interactions)



    # Optionally filter out news with no source_name if ansa is False
    if not ansa:
        filtered_news_df = filtered_news_df.filter(
            (col('source_name').isNotNull()) &
              (col('source_name') != "")
        #(~col('news_id').isin(seen_and_liked_news_ids))

        )

    # Filter processed news DataFrame based on user preferences
    filtered_news_df = processed_news_df.filter(
        (col('prediction').isin(categories)) 
        &
        (col('sentiment_label').isin(sentiments))


    )
    print('Filtered df is:')
    filtered_news_df.show()


    filtered_news = filtered_news_df.collect()
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!',filtered_news)
    recommendations = []

    if not filtered_interactions:
        recommended_news_ids=[news["id"] for news in filtered_news]
    else:
        print('In the else case')

        for news in filtered_news:
            news_id = news["id"]
            news_features = news["features"]

            similarity = look_for_similarity(news_features.asDict(), 
                                            filtered_interactions)
            print('similarity=',similarity)
            
            recommendations.append((news_id, similarity))

        recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
        recommended_news_ids = [values[0] for values in recommendations]

        print('%%%%%%%%%%The recommendations are: ',recommendations)
        #result = [row.asDict() for row in filtered_news_df.collect()]

        # Collect news IDs that match user preferences
        #recommended_news_ids = [row.id for row in filtered_news_df.select("id").collect()]
        
    print('Recommended News ids for:',user.email,':',recommended_news_ids)

    # Update recommended_news in user object
    user.recommended_news = recommended_news_ids

    # Update user object in MongoDB
    user_preferences_collection.update_one(
        {'_id': user_id},
        {'$set': {'recommended_news': recommended_news_ids}}
    )

# Stop the Spark Session
spark.stop()
