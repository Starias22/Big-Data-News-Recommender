from kafka import KafkaConsumer
import json
from pathlib import Path
import sys

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[1]
sys.path.append(str(src_path))

from models.filtered_news import FilteredNews
from db.filtered_news_db import FilteredNewsDB



def persist_filtered_news(topics=None ,
       servers=None,timeout_ms=5000):
     
    if topics is None and servers  is None:
         # Load the configuration from the JSON file
        with open('../../config/config.json', 'r') as config_file:
            config = json.load(config_file)

            # List of topics to subscribe to
            topics = [config["filtered_news_topic"]]
            servers=config["kafka_bootstrap_servers"]
            
    # Initialize the consumer
    consumer = KafkaConsumer(
        *topics,  # Unpack the list of topics
        bootstrap_servers=servers,
        auto_offset_reset='earliest',  # Start reading from the earliest message
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        consumer_timeout_ms=timeout_ms
        
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

    print(f"{n + 1} filtered news to MongoDB")

if __name__=="__main__":
    persist_filtered_news()