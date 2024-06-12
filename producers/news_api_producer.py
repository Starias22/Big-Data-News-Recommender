from datetime import datetime, timedelta
import pytz
from newsapi import NewsApiClient
import json
import pandas as pd
import redis
from kafka import KafkaProducer

# Load the configuration from the JSON file
with open('../config/config.json', 'r') as config_file:
    config = json.load(config_file)

# Init NewsAPI client
newsapi = NewsApiClient(api_key=config['newsapi_key'])

# Get current time in UTC
now = datetime.now(pytz.utc)

# Calculate the time one day ago
period_ago = now - timedelta(hours=25)

# Format the dates in the required format
from_param = period_ago.strftime('%Y-%m-%dT%H:%M:%S')
to = now.strftime('%Y-%m-%dT%H:%M:%S')

articles_list = []
status_dict = {}
num_results_dict = {}
total_results = 0

for lang in config["languages"][:1]:
    results = []
    for query in config["query"]:
        response = newsapi.get_everything(
            q=query,
            from_param=from_param,
            to=to,
            language=lang,
            sort_by='relevancy',
            page=config["page"],
            page_size=config["page_size"]
        )

        status = response['status']
        total_results_query = response['totalResults']
        articles = response['articles']

        if articles:
            results.extend(articles)

    print(f"{lang} got {len(results)} articles")

    if results:
        articles_df = pd.DataFrame(results)
        articles_df['lang'] = lang

        # Add source_id and source_name columns
        articles_df['source_id'] = articles_df['source'].apply(lambda x: x['id'] if x else None)
        articles_df['source_name'] = articles_df['source'].apply(lambda x: x['name'] if x else None)
        articles_df.drop(columns=['source'], inplace=True)

        articles_list.append(articles_df)

        status_dict[lang] = status
        num_results_dict[lang] = len(results)
        total_results += len(results)

if articles_list:
    articles = pd.concat(articles_list, axis=0, ignore_index=True)
    articles.replace(config["null_replacements"], inplace=True)
    articles.rename(columns={
        'urlToImage': 'img_url',
        'publishedAt': 'publication_date'
    }, inplace=True)

    articles['producer'] = 'NewsAPI'
else:
    articles = pd.DataFrame()

print('Articles:', articles, sep="\n")

print(status_dict)
print(num_results_dict)
print(total_results)

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=config['kafka_bootstrap_servers'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send articles to Kafka
for _, article in articles.iterrows():
    standardized_news = {
        "title": article['title'],
        "description": article['description'],
        "content": article["content"],
        "source_name": article['source_name'],
        "source_id": article['source_id'],
        "url": article['url'],
        "img_url": article['img_url'],
        "publication_date": article['publication_date'],
        "lang": article['lang'],
        "producer": article['producer']
    }
    producer.send(config['raw_news_topic'], standardized_news)

print(f"{total_results} news articles sent by NewsAPI producer")

producer.flush()

# Store metadata to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
current_id = redis_client.incr('date_id')
metadata = {
    'id': current_id,
    'date': now.strftime('%Y-%m-%dT%H:%M:%S'),
    'status': status_dict,
    'num_results': num_results_dict,
    'total': total_results
}
redis_client.set(f'news_metadata:{current_id}', json.dumps(metadata))
print('Metadata stored to Redis:', metadata)
