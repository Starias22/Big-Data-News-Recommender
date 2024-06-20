from kafka import KafkaConsumer
import json
from pathlib import Path
import sys

# Add the root directory to the Python path
root_path = Path(__file__).resolve().parents[2]
sys.path.append(str(root_path))

from src.models.user import User
from src.db.user_db import UserDB

from src.models.filtered_news import FilteredNews
from config.config import KAFKA_BOOTSTRAP_SERVERS,PROCESSED_NEWS_TOPIC

def fetch_recommended_news(user_email,topics=None, servers=None, 
                             timeout_ms=5000):

    user = User(email=user_email)
    recommended_news_ids = UserDB().find_user_by_email(user.email).recommended_news
    recommended_news = []

    # Ensure the path to the config file is correct
    config_path = root_path / 'config' / 'config.json'
    print(f"Looking for config file at: {config_path}")
    topics = [PROCESSED_NEWS_TOPIC]
    servers = KAFKA_BOOTSTRAP_SERVERS

    # Initialize the consumer
    consumer = KafkaConsumer(
        *topics,  # Unpack the list of topics
        bootstrap_servers=servers,
        auto_offset_reset='earliest',  # Start reading from the earliest message
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        consumer_timeout_ms=timeout_ms  # Stop after timeout_ms of inactivity
    )

    # Consume messages from the subscribed topics
    if recommended_news:
        for n, message in enumerate(consumer):
            filtered_news_data = message.value
            print(f"Received message {n + 1}")
            print(filtered_news_data)
            print('The id is',filtered_news_data['id'])
            print(recommended_news_ids)
            filtered_news_data['_id'] = filtered_news_data.pop('id')
            if filtered_news_data['_id'] in recommended_news_ids:
                #filtered_news_data['_id'] = filtered_news_data.pop('id')

                print('@@@@@@@@@@@@@@@@@@@@@')
                filtered_news = FilteredNews.from_dict(filtered_news_data)

                recommended_news.append(filtered_news)
    else:
        # Consume messages from the subscribed topics
        for n, message in enumerate(consumer):
            filtered_news_data = message.value
            print(f"Received message {n + 1}")
            print(filtered_news_data)
            print('The id is',filtered_news_data['id'])
            print(recommended_news_ids)
            filtered_news_data['_id'] = filtered_news_data.pop('id')
            print('@@@@@@@@@@@@@@@@@@@@@')
            filtered_news = FilteredNews.from_dict(filtered_news_data)

            recommended_news.append(filtered_news)
    return recommended_news

if __name__ == "__main__":
    news = fetch_recommended_news()
    print(news)
    print(len(news), 'recommended news')
