from kafka import KafkaConsumer
import json
from pathlib import Path
import sys

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[1]
sys.path.append(str(src_path))

from profiles.filtered_news import FilteredNews  # Make sure to import the FilteredNews class from the appropriate module
from db.filtered_news_db import FilteredNewsDB  # Ensure the correct path to FilteredNewsDB

# Load the configuration from the JSON file
with open('../../config/config.json', 'r') as config_file:
    config = json.load(config_file)

# List of topics to subscribe to
topics = [config["filtered_news_topic"]]

# Initialize the consumer
consumer = KafkaConsumer(
    *topics,  # Unpack the list of topics
    bootstrap_servers=config["kafka_bootstrap_servers"],
    auto_offset_reset='earliest',  # Start reading from the earliest message
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Kafka Consumer Initialized")

# Initialize MongoDB filtered news database
filtered_news_db = FilteredNewsDB()

print(f"Connected to MongoDB")

# Consume messages from the subscribed topics
for n, message in enumerate(consumer):
    filtered_news_data = message.value
    print(f"Received message {n + 1}: {filtered_news_data}")

    # Deserialize the message into a FilteredNews object
    filtered_news = FilteredNews.from_dict(filtered_news_data)

    # Insert filtered news into MongoDB
    result = filtered_news_db.create_filtered_news(filtered_news)
    print(f"Inserted filtered news with ID: {result}")

print(f"Processed {n + 1} messages")
