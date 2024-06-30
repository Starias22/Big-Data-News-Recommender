import json
import pandas as pd
from datetime import datetime, timedelta
import pytz
from GoogleNews import GoogleNews

from pathlib import Path
import sys

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))
from config.config import NULL_REPLACEMENTS, LANGUAGES, QUERY, PAGE, PAGE_SIZE


class NewsProducer:
    def __init__(self, page=None, page_size=None, null_replacements=None, languages=None, query=None):
        self.page = PAGE
        self.page_size = PAGE_SIZE
        self.null_replacements = NULL_REPLACEMENTS
        self.languages = LANGUAGES
        self.query = QUERY

        # Get current time in UTC
        self.now = datetime.now(pytz.utc)

        # Calculate the time one day ago
        self.period_ago = self.now - timedelta(hours=25)

    def fetch_articles(self, lang, query):
        googlenews = GoogleNews(period='25h', lang=lang)
        googlenews.search(query)
        results = googlenews.result()
        googlenews.clear()
        return results

    def process_articles(self, articles):
        articles_df = pd.DataFrame(articles)
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
        articles_df['content'] = 'From Google News'
        articles_df.replace(self.null_replacements, inplace=True)
        return articles_df

    def run(self):
        articles_list = []
        num_results_dict = {}
        total_results = 0
        languages = self.languages
        queries = self.query

        for lang in languages[:1]:
            results = []
            for query in queries[:1]:
                articles = self.fetch_articles(lang, query)
                if articles:
                    results.extend(articles)
            
            if results:
                processed_articles = self.process_articles(results)
                processed_articles['lang'] = lang
                articles_list.append(processed_articles)
                num_results_dict[lang] = len(processed_articles)
                total_results += len(processed_articles)
        
        if articles_list:
            all_articles = pd.concat(articles_list, axis=0, ignore_index=True)
        else:
            all_articles = pd.DataFrame()
        
        print(all_articles['publication_date'])

       

        print(f"{total_results} news articles processed from Google News")

# Example usage
if __name__ == "__main__":
    news_producer = NewsProducer()
    news_producer.run()
