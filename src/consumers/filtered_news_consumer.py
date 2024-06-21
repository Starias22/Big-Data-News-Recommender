from kafka import KafkaConsumer
import json
from pathlib import Path
import sys

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))

from src.models.filtered_news import FilteredNews
from src.db.filtered_news_db import FilteredNewsDB
from config.config import KAFKA_BOOTSTRAP_SERVERS,FILTERED_NEWS_TOPIC


def persist_filtered_news(topics=[FILTERED_NEWS_TOPIC] ,
       servers=KAFKA_BOOTSTRAP_SERVERS):
     
            
    # Initialize the consumer
    consumer = KafkaConsumer(
        *topics,  # Unpack the list of topics
        bootstrap_servers=servers,
        auto_offset_reset='earliest',  # Start reading from the earliest message
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        
    )

    print("Kafka Consumer Initialized")

    # Initialize MongoDB filtered news database
    filtered_news_db = FilteredNewsDB()

    #print(f"Connected to MongoDB")
    
    # Consume messages from the subscribed topics
    for n, message in enumerate(consumer):
        print('******')
        filtered_news_data = message.value
        print(f"Received message {n + 1}: {filtered_news_data}")

        # Deserialize the message into a FilteredNews object
        #filtered_news_data['_id'] = filtered_news_data.pop('id')
        #filtered_news = FilteredNews.from_dict_persist(filtered_news_data)

        # Insert filtered news into MongoDB
        #result = filtered_news_db.create_filtered_news(filtered_news)
        #print(f"Inserted filtered news with ID: {result}")

    #print(f"{n + 1} filtered news saved to MongoDB")

if __name__=="__main__":
    persist_filtered_news()