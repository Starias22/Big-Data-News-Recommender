from pymongo import MongoClient
import sys
from pathlib import Path

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))

from src.models.filtered_news import FilteredNews  

from config.config import MONGO_DB_NAME,MONGO_DB_URI
class FilteredNewsDB:
    def __init__(self, uri=MONGO_DB_URI, db_name=MONGO_DB_NAME):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        #print(MONGO_DB_URI)
        #print(MONGO_DB_NAME)

    def create_filtered_news(self, news):
        news_dict = news.to_dict_persist()
        result = self.db.filtered_news.insert_one(news_dict)
        return result.inserted_id
    
    def create_many_filtered_news(self, news_list):
        news_dicts = [news.to_dict_persist() for news in news_list]
        result = self.db.filtered_news.insert_many(news_dicts)
        return result.inserted_ids

    def find_filtered_news_by_id(self, news_id):
        news_data = self.db.filtered_news.find_one({"news_id": news_id})
        if news_data:
            return FilteredNews.from_dict(news_data)
        return None

    def find_filtered_news_by_title(self, title):
        news_data = self.db.filtered_news.find_one({"title": title})
        if news_data:
            return FilteredNews.from_dict(news_data)
        return None

    def retrieve_all_filtered_news(self):
        news_cursor = self.db.filtered_news.find()
        return [FilteredNews.from_dict(news_data) for news_data in news_cursor]


"""# Example usage
if __name__ == "__main__":
    # Create an instance of FilteredNewsDB
    filtered_news_db = FilteredNewsDB()

    # Create a FilteredNews instance
    news_instance = FilteredNews(
        news_id="12345",
        title="Sample Newtle",
        description="This is a sample news description.",
        source_id="source_001",
        source_name="Sample Source",
        url="http://example.com/sample-news",
        img_url="http://example.com/sample-image.jpg",
        publication_date="2024-06-16",
        lang="en"
    )

    # Insert the news instance into the database
    news_id = filtered_news_db.create_filtered_news(news_instance)
    print(f"Inserted news with ID: {news_id}")

    # Retrieve the news by ID
    retrieved_news = filtered_news_db.find_filtered_news_by_id("12345")
    if retrieved_news:
        retrieved_news.display()

    # Retrieve all news
    all_news = filtered_news_db.retrieve_all_filtered_news()
    for news in all_news:
        news.display()
"""