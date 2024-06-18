from kafka import KafkaConsumer
import json
from pathlib import Path
import sys

# Add the root directory to the Python path
root_path = Path(__file__).resolve().parents[2]
sys.path.append(str(root_path / 'src'))

from models.user import User
from db.user_db import UserDB

from models.filtered_news import FilteredNews
from db.filtered_news_db import FilteredNewsDB

def fetch_recommended_news(topics=None, servers=None, 
                           timeout_ms=5000, user_email='adedeezechiel@gmail.com'):
    user = User(email=user_email)
    recommended_news_ids = UserDB().find_user_by_email(user=user).recommended_news
    recommended_news = []

    # Ensure the path to the config file is correct
    config_path = root_path / 'config' / 'config.json'
    print(f"Looking for config file at: {config_path}")

    if topics is None and servers is None:
        # Load the configuration from the JSON file
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            # List of topics to subscribe to
            topics = [config["processed_news_topic"]]
            servers = config["kafka_bootstrap_servers"]

    # Initialize the consumer
    consumer = KafkaConsumer(
        *topics,  # Unpack the list of topics
        bootstrap_servers=servers,
        auto_offset_reset='earliest',  # Start reading from the earliest message
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        consumer_timeout_ms=timeout_ms  # Stop after timeout_ms of inactivity
    )

    # Consume messages from the subscribed topics
    for n, message in enumerate(consumer):
        filtered_news_data = message.value
        print(f"Received message {n + 1}")
        if filtered_news_data['id'] in recommended_news_ids:
            filtered_news = FilteredNews.from_dict(filtered_news_data)

            recommended_news.append(filtered_news)

    return recommended_news

if __name__ == "__main__":
    news = fetch_recommended_news()
    print(news)
    print(len(news), 'recommended news')
