from kafka import KafkaConsumer
import json
from pathlib import Path
import sys

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))

from src.models.filtered_news import FilteredNews
from src.db.filtered_news_db import FilteredNewsDB
from config.config import KAFKA_BOOTSTRAP_SERVERS,PROCESSED_NEWS_TOPIC


def persist_filtered_news(topics=[PROCESSED_NEWS_TOPIC] ,
       servers=KAFKA_BOOTSTRAP_SERVERS):
     
            
    # Initialize the consumer
    consumer = KafkaConsumer(
        *topics,  # Unpack the list of topics
        bootstrap_servers=servers,
        auto_offset_reset='earliest',  # Start reading from the earliest message
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        
    )

    print("Kafka Consumer Initialized")

    
    # Consume messages from the subscribed topics
    for n, message in enumerate(consumer):
        print('******')
        filtered_news_data = message.value
        print(f"Received message {n + 1} from {PROCESSED_NEWS_TOPIC}: {filtered_news_data}")

if __name__=="__main__":
    persist_filtered_news()