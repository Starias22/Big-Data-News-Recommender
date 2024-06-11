
'''
Documentations:https://github.com/mattlisiv/newsapi-python
'''
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
# Init


# Get current time in UTC
now = datetime.now(pytz.utc)

# Calculate the time one hour ago
period_ago = now - timedelta(hours=25)

# Format the dates in the required format
from_param = period_ago.strftime('%Y-%m-%dT%H:%M:%S')
to = now.strftime('%Y-%m-%dT%H:%M:%S')
newsapi = NewsApiClient(api_key=config['newsapi_key'])
articles_list=[]


articles_list = []
status_dict = {}
num_results_dict = {}
total_results = 0



for lang in config["languages"]:
    articles = newsapi.get_everything(q=config["query"],
                            from_param=from_param,
                            to=to,
                            language=lang,
                            sort_by='relevancy',
                            page=config["page"],
                            page_size=config["page_size"])

    status,num_results,articles=articles['status'],articles['totalResults'],articles['articles']
    print('Status:',status)
    print('Number of results:',num_results)
    

    if num_results!=0:
        articles = list(map(
            lambda article: {**article, 
                             'source_id': article['source']['id'],
                             'source_name': article['source']['name'],
                             'source': None
                             },
            articles
        ))
        #update_article = lambda article: {**article, 'source': article['source']['name']}

        #updated_articles = articles.map(update_article).collect()
        
        print('The lenght is:',len(articles))
        print('xxxxx:',articles)
        articles = pd.DataFrame(articles)
        print('********The shape is:',articles.shape)

        
        articles.drop('source', axis=1, inplace=True)
        articles.rename(columns={'urlToImage': 'img_url',
                            'publishedAt': 
                            'publication_date'},
                            inplace=True)
        articles['lang']=lang
        print(articles.keys())
        articles_list.append(articles)

    status_dict[lang] = status
    num_results_dict[lang] = num_results
    total_results += num_results
    print('Status:', status)
    print('Number of results:', num_results)


if len(articles_list)==0:
    articles=pd.DataFrame()
else:
    articles =pd.concat(articles_list, axis=0, ignore_index=True)
    # Replacements dictionary

    articles.replace(config["null_replacements"], inplace=True)

print('Articles:',articles,sep="\n")

print(status_dict)
print(num_results_dict)
print(total_results)


# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers= config['kafka_bootstrap_servers'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print(producer)

n=0
# Send articles to Kafka
for _, article in articles.iterrows():
    standardized_news = {
        "title": article['title'],
        "description": article['description'],
        "content":article["content"],
        "source_name": article['source_name'],
        "source_id": article['source_id'],
        "url": article['url'],
        "img_url": article['img_url'],
        "publication_date": article['publication_date'],
        "lang": article['lang']

    }
    producer.send(config['news_topic'], standardized_news)
    n+=1
    print(n)

producer.flush()

print('Done')

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
# Store metadata to Redis
current_id = redis_client.incr('news_id')
metadata = {
    'id': current_id,
    'date': now.strftime('%Y-%m-%dT%H:%M:%S'),
    'status': status_dict,
    'num_results': num_results_dict,
    'num_results': 3,
    'total': total_results

}
redis_client.set(f'news_metadata:{current_id}', json.dumps(metadata))
print('Metadata stored to Redis:', metadata)
