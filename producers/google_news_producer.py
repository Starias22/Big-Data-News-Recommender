from GoogleNews import GoogleNews
import pandas as pd
from datetime import datetime, timedelta
import pytz 
from newsapi import NewsApiClient
import json
import redis
from kafka import KafkaProducer

# Load the configuration from the JSON file
with open('../config/config.json', 'r') as config_file:
    config = json.load(config_file)


# Get current time in UTC
now = datetime.now(pytz.utc)

# Calculate the time one hour ago
period_ago = now - timedelta(hours=25)

# Format the dates in the required format
#from_param = period_ago.strftime('%Y-%m-%dT%H:%M:%S')
#to = now.strftime('%Y-%m-%dT%H:%M:%S')
newsapi = NewsApiClient(api_key=config['newsapi_key'])
articles_list = []
status_dict = {}
num_results_dict = {}
total_results = 0

for lang in config["languages"][:1]:

    results=[]

    for query in config["query"]:
        googlenews = GoogleNews(period='25h', lang=lang)

        googlenews.search(query)
        results.extend( googlenews.result(query))
        googlenews.clear()
    print(lang,'got',len(results))

    if len(results):
        print(results[0]['datetime'])
        print(type(results[0]['datetime']))

        results_df = pd.DataFrame(results)
        results_df['lang'] = lang
        articles_list.append(results_df)
        num_results_dict[lang] = len(results_df)
        total_results += num_results_dict[lang]

if articles_list:
    articles = pd.concat(articles_list, axis=0, ignore_index=True)
else:
    articles = pd.DataFrame()

articles.drop('date', axis=1, inplace=True, errors='ignore')

articles.rename(columns={
    'urlToImage': 'img_url',
    'publishedAt': 'publication_date',
    'datetime': 'publication_date',
    'link': 'url',
    'img': 'img_url',
    'desc': 'description',
    'media': 'source_name'
}, inplace=True)

# Replace NaN with None and convert datetime to string
articles['publication_date'] = articles['publication_date'].apply(
    lambda x: x if isinstance(x, str) else (x.strftime('%Y-%m-%d %H:%M:%S') if pd.notna(x) else None)
)

articles['source_id'] = articles['author'] = articles['source_name']
articles['content'] = 'From Google News API'
articles['producer'] = 'GoogleNewsAPI'
articles.replace(config["null_replacements"], inplace=True)

print(articles.keys())
print(num_results_dict)
print(total_results)

print(articles['publication_date'])

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=config['kafka_bootstrap_servers'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print(producer)

#n = 0
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
        "producer":article['producer'] 

    }
    producer.send(config['raw_news_topic'], standardized_news)
    #n += 1

producer.flush()
print(total_results,'news sent by GoogleNewsAPI producer')


redis_client = redis.StrictRedis(host='localhost', port=6379, db=1)
# Store metadata to Redis
current_id = redis_client.incr('day_id')
metadata = {
    'id': current_id,
    'date': now.strftime('%Y-%m-%dT%H:%M:%S'),
    
    'num_results': num_results_dict,
    'total': total_results
}
redis_client.set(f'news_metadata:{current_id}', json.dumps(metadata))
print('Metadata stored to Redis:', metadata)