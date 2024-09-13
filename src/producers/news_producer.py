import json
import redis
from kafka import KafkaProducer
import pandas as pd
from datetime import datetime, timedelta
import pytz
from newsapi import NewsApiClient
from GoogleNews import GoogleNews

from pathlib import Path
import sys

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))
from config.config import NEWSAPI_KEYS,RAW_NEWS_TOPIC,NULL_REPLACEMENTS,LANGUAGES,QUERY,PAGE,PAGE_SIZE,REDIS_HOST,KAFKA_BOOTSTRAP_SERVERS


class NewsProducer:
    def __init__(self):

        self.topic=RAW_NEWS_TOPIC
        self.page=PAGE
        self.page_size=PAGE_SIZE
        self.null_replacements=NULL_REPLACEMENTS
        self.languages=LANGUAGES
        self.query=QUERY
        self.page=self.page       
        # Initialize Redis client

        # Initialize Kafka Producer
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # Initialize NewsAPI client
        self.newsapi = NewsApiClient(api_key=NEWSAPI_KEYS[0])
        
        # Get current time in UTC
        self.now = datetime.now(pytz.utc)

        # Calculate the time one day ago
        self.period_ago = self.now - timedelta(hours=25)
        
        # Format the dates in the required format
        self.from_param = self.period_ago.strftime('%Y-%m-%dT%H:%M:%S')
        self.to = self.now.strftime('%Y-%m-%dT%H:%M:%S')

        
    def get_max_news_id(self):
        max_news_id = self.redis_client.get('max_news_id')
        if max_news_id is None:
            return 0
        else:
            return int(json.loads(max_news_id)['value'])

    def db_connection(self,db) :
        self.redis_client = redis.StrictRedis(host=REDIS_HOST, port=6379, db=db)


    def update_max_news_id(self, news_id):
        self.redis_client.set('max_news_id', json.dumps({'value': news_id}))

    def store_metadata(self, metadata, prefix):
        current_id = self.redis_client.incr('id')
        self.redis_client.set(f'{prefix}_metadata:{current_id}', json.dumps(metadata))
        print(f'Metadata stored to Redis: {metadata}')

    def send_to_kafka(self, articles, news_id_prefix):
        
        max_news_id = self.get_max_news_id()
        news_id = max_news_id + 1

        for _, article in articles.iterrows():
            standardized_news = {
                "title": article['title'],
                "description": article['description'],
                "content": article["content"],
                "source_name": article['source_name'],
                "url": article['url'],
                "img_url": article['img_url'],
                "publication_date": article['publication_date'],
                "lang": article['lang'],
                "id": f"{news_id_prefix}_{news_id}",
                "author":article['author'],
            }
            self.producer.send(self.topic, standardized_news)
            news_id += 1
        
        self.producer.flush()
        self.update_max_news_id(news_id - 1)

    def fetch_articles(self, source, lang, query):
        if source == 'google_news':
            googlenews = GoogleNews(period='25h', lang=lang)
            googlenews.search(query)
            results = googlenews.result()
            googlenews.clear()
            return results
        elif source == 'newsapi':
            response = self.newsapi.get_everything(
                q=query,
                from_param=self.from_param,
                to=self.to,
                language=lang,
                sort_by='relevancy',
                page=self.page,
                page_size=self.page_size
            )
            return response['articles'] if response['status'] == 'ok' else []
        else:
            raise ValueError("Unknown news source")

    def process_articles(self, articles, source):
        articles_df = pd.DataFrame(articles)
        if source == 'google_news':
            articles_df.rename(columns={
            'urlToImage': 'img_url',
            'datetime': 'publication_date',
            'link': 'url',
            'img': 'img_url',
            'desc': 'description',
            'media': 'source_name'
            }, inplace=True)
            articles_df['author'] = None


            articles_df['publication_date'] = articles_df['publication_date'].apply(lambda x: int(x.timestamp()) if pd.notna(x) else None)
            articles_df['content']='From Google News'
        elif source == 'newsapi':
            articles_df.rename(columns={
            'urlToImage': 'img_url',
            'publishedAt': 'publication_date'
            }, inplace=True)
            fmt = "%Y-%m-%dT%H:%M:%SZ"
            articles_df['publication_date'] = articles_df['publication_date'].apply(lambda x: int(datetime.strptime(x, fmt).timestamp()))
            articles_df['source_name'] = articles_df['source'].apply(lambda x: x['name'] if x else None)
            articles_df.drop(columns=['source'], inplace=True)
        
        articles_df.replace(self.null_replacements, inplace=True)
        return articles_df

    def run(self, source):
        articles_list = []
        num_results_dict = {}
        total_results = 0
        languages=self.languages
        queries=self.query

        for lang in languages[:1]:
            results = []
            for query in queries[:1]:
                articles = self.fetch_articles(source, lang, query)
                if articles:
                    results.extend(articles)
            
            if results:
                processed_articles = self.process_articles(results, source)
                processed_articles['lang'] = lang
                articles_list.append(processed_articles)
                num_results_dict[lang] = len(processed_articles)
                total_results += len(processed_articles)
        
        if articles_list:
            all_articles = pd.concat(articles_list, axis=0, ignore_index=True)
        else:
            all_articles = pd.DataFrame()
        print(all_articles)
        self.send_to_kafka(all_articles, source)

        metadata = {
            'date': int(self.now.timestamp()),
            'num_results': num_results_dict,
            'total': total_results
        }
        self.store_metadata(metadata, source)

        print(f"{total_results} news articles sent by {source.capitalize()} producer")
