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
from config.config import KAFKA_BOOTSTRAP_SERVERS,AVAILABLE_NEWS_TOPIC,TIME_OUT_MS

def fetch_recommended_news(user_id,topics=None, servers=None):

    user = User(user_id=user_id)
    recommended_news_ids = UserDB().find_user_by_id(user.id).recommended_news
    recommended_news = []
    print('The recommended news ids:',recommended_news_ids)

    
    topics = [AVAILABLE_NEWS_TOPIC]
    servers = KAFKA_BOOTSTRAP_SERVERS

    # Initialize the consumer
    consumer = KafkaConsumer(
        *topics,  # Unpack the list of topics
        bootstrap_servers=servers,
        auto_offset_reset='earliest',  # Start reading from the earliest message
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        consumer_timeout_ms=TIME_OUT_MS  # Stop after timeout_ms of inactivity
    )

    # Consume messages from the subscribed topics
    if recommended_news_ids:
        for n, message in enumerate(consumer):
            filtered_news_data = message.value
            print(f"Received message {n + 1}")
            print(filtered_news_data)
            print('_____________________________________________')
            print('+++++++++++The sentiment is',filtered_news_data['sentiment_score'])

            print('**************The id is',filtered_news_data['id'])
            print(recommended_news_ids)
            filtered_news_data['_id'] = filtered_news_data.pop('id')
            if filtered_news_data['_id'] in recommended_news_ids:
                #filtered_news_data['_id'] = filtered_news_data.pop('id')

                print('+++++++++++++++++++++++++')
                filtered_news = FilteredNews.from_dict(filtered_news_data)
                print(filtered_news.sentiment)

                recommended_news.append(filtered_news)
    else:
        # Consume messages from the subscribed topics
        for n, message in enumerate(consumer):
            filtered_news_data = message.value
            
            print(f"Received message {n + 1}")
            print(filtered_news_data)
            print(recommended_news_ids)
            filtered_news_data['_id'] = filtered_news_data.pop('id')
            
            filtered_news = FilteredNews.from_dict(filtered_news_data)

            recommended_news.append(filtered_news)
    return recommended_news

if __name__ == "__main__":
    pass
    #news = fetch_recommended_news(user_id='6675d6cbd31adca141eeeb1b')
    #print(news)
    #print(len(news), 'recommended news')
    #print(news[0].sentiment)
