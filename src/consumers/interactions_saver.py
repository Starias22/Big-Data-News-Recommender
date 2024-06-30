from kafka import KafkaConsumer
import json
from pathlib import Path
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType, DoubleType
from pyspark.sql.functions import struct, collect_list, col
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, udf
from pyspark.sql.types import StructType, StructField, IntegerType

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))

from src.models.interaction import Interaction
from src.db.interaction_db import InteractionDB
from src.db.user_db import UserDB
from src.models.interaction import Interaction
from config.config import KAFKA_BOOTSTRAP_SERVERS, INTERACTIONS_TOPIC, PROCESSED_NEWS_TOPIC

# List of topics to subscribe to
topics = [INTERACTIONS_TOPIC]

# Initialize the consumer for interactions
interaction_consumer = KafkaConsumer(
    *topics,  # Unpack the list of topics
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',  # Start reading from the earliest message
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    consumer_timeout_ms=1000
)

# Initialize the consumer for processed news
news_consumer = KafkaConsumer(
    PROCESSED_NEWS_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    consumer_timeout_ms=1000,
    group_id='interaction_consumers_group'
)

print("Kafka Consumers Initialized")

# Initialize MongoDB interaction database
interaction_db = InteractionDB()

print("Connected to MongoDB")
interactions_list = []
news_features_list = []

# Initialize counter
n = 0

# Consume messages from the interactions topic
for n, message in enumerate(interaction_consumer):
    interaction_data = message.value
    print(f"Received interaction message {n + 1}: {interaction_data}")
    interactions_list.append(interaction_data)

print(f"Processed {n} interaction messages")
print('The interactions list is',interactions_list)
# Consume messages from the processed news topic
for n, message in enumerate(news_consumer):
    news_data = message.value
    print(f"Received news message {n + 1}: {news_data}")
    news_features_list.append(news_data)

print(f"Processed {n} news messages")

# Retrieve user IDs from MongoDB
user_ids = UserDB().retrieve_user_ids()
print('User IDs are:', user_ids)

# Initialize Spark session
spark = SparkSession.builder.appName("InteractionsApp").getOrCreate()

# Define feature schema for DataFrame
feature_schema = StructType([
    StructField("size", IntegerType(), True),
    StructField("indices", ArrayType(IntegerType()), True),
    StructField("values", ArrayType(DoubleType()), True)
])

# Define schema for interactions DataFrame
interaction_schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("news_id", StringType(), True),
    StructField("action", IntegerType(), True),
    StructField("date", IntegerType(), True),
    StructField("features", feature_schema, True),
])

# Define schema for news features DataFrame
news_schema = StructType([
    StructField("id", StringType(), True),
    StructField("features", feature_schema, True),
])

# Extract all fields from interactions_list
interaction_data_list = [(interaction['user_id'], interaction['news_id'], interaction['action'], interaction['date'], interaction.get('features')) for interaction in interactions_list]

# Extract all fields from news_features_list
news_data_list = [(news['id'], news['features']) for news in news_features_list]

# Create Spark DataFrames
interactions_df = spark.createDataFrame(interaction_data_list, schema=interaction_schema)
news_df = spark.createDataFrame(news_data_list, schema=news_schema)

# Rename 'id' column in news_df to 'news_id' and 'features' to 'news_features'
news_df = news_df.withColumnRenamed('id', 'news_id').withColumnRenamed('features', 'news_features')

# Join the interactions DataFrame with the news features DataFrame on the `news_id` column
combined_df = interactions_df.join(news_df, on='news_id', how='left')

combined_df = combined_df.drop('features').withColumnRenamed('news_features', 'features')
print('Combined df is',combined_df)
print('Combined df schema:')
combined_df.printSchema()
print('Combined df data:')
combined_df.show(truncate=False)

interaction_df=combined_df.select(['news_id','features','date']).dropDuplicates(subset=['news_id']).orderBy('date', ascending=True)

#interaction_df.show()

print('Interaction df schema:')
interaction_df.printSchema()
print('Interaction df data:')
interaction_df.show(truncate=False)

# Convert each row of the DataFrame into an Interaction object and insert into MongoDB
for row in interaction_df.collect():
    interaction = Interaction(
        news_id=row['news_id'],
        features=row['features'],
        date=row['date']
    )
    interaction_id = interaction_db.insert_interaction(interaction)
    print(f"Inserted interaction with ID: {interaction_id}")


# Group by `user_id` and `news_id` and collect the interactions as lists
grouped_df = combined_df.groupBy("user_id", "news_id").agg(
    collect_list(struct("action", "date")).alias("actions")
)

print('The grouped df is')
grouped_df.show(truncate=False)

# Function to apply the deduplication logic
def deduplicate(actions):
    actions.sort(key=lambda x: x.date)  # Sort by date
    non_neutral_actions = [action for action in actions if action.action != 0]
    if non_neutral_actions:
        return non_neutral_actions[-1]  # Keep the latest non-neutral action
    return actions[-1]  # If no non-neutral actions, keep the latest action

# Function to apply the deduplication logic
def deduplicate(actions):
    actions.sort(key=lambda x: x.date)  # Sort by date
    non_neutral_actions = [action for action in actions if action.action != 0]
    if non_neutral_actions:
        return non_neutral_actions[-1]  # Keep the latest non-neutral action
    return actions[-1]

# Register the function as a UDF
deduplicate_udf = udf(deduplicate, StructType([
    StructField("action", IntegerType(), True),
    StructField("date", IntegerType(), True),
    #StructField("features", feature_schema, True),
]))

# Apply the deduplication function to the grouped data
deduplicated_df = grouped_df.withColumn("deduplicated", deduplicate_udf(col("actions"))).select("user_id", "news_id", "deduplicated.*")

# Join back with the news_df to get features
final_df = deduplicated_df.join(news_df, on='news_id', how='left')

# Apply the deduplication function to the grouped data
#deduplicated_df = grouped_df.withColumn("deduplicated", deduplicate_udf(col("actions"))).select("user_id", "news_id", "deduplicated.*")

# Group by `user_id` and collect the deduplicated interactions
final_grouped_df = deduplicated_df.groupBy("user_id").agg(
    collect_list(struct("news_id", "action", "date")).alias("interactions")
)

print('The final grouped df is')
final_grouped_df.printSchema()
final_grouped_df.show(truncate=False)

# Collect the final grouped DataFrame into a list of rows
final_grouped_rows = final_grouped_df.collect()

# Initialize the UserDB instance
user_db = UserDB()

# Add seen news for each user ID in the grouped DataFrame
for row in final_grouped_rows:
    user_id = row['user_id']
    interactions = row['interactions']
    news_actions = {interaction['news_id']: interaction['action'] for interaction in interactions}
    print('News actions:',news_actions)
    user_db.add_seen_news(user_id, news_actions)

# Stop the Spark session
spark.stop()