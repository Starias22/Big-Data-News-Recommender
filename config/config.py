import json
import os

def load_config(filepath='config.json'):
    # Use absolute path to ensure we find the file
    abs_filepath = os.path.join(os.path.dirname(__file__), filepath)
    with open(abs_filepath, 'r') as file:
        return json.load(file)

# Load configurations from config.json
config = load_config()

# Assign configurations to variables
NEWSAPI_KEYS = [
    config.get("__newsapi_key", ""),
    config.get("_newsapi_key", ""),
    config.get("___newsapi_key", ""),
    config.get("newsapi_key", "")
]
NEWSDATAAPI_KEY = config.get("newsdataapi_key", "")
LANGUAGES = config.get("languages", [])
PAGE_SIZE = config.get("page_size", 10)
HOURS_PERIOD = config.get("hours_period", 25)  
QUERY = config.get("query", [])
PAGE = config.get("page", 1)  # Example default value
RAW_NEWS_TOPIC = config.get("raw_news_topic", "")
FILTERED_NEWS_TOPIC = config.get("filtered_news_topic", "")
PROCESSED_NEWS_TOPIC = config.get("processed_news_topic", "")
INTERACTIONS_TOPIC = config.get("interactions_topic", "")
NULL_REPLACEMENTS = config.get("null_replacements", {})
KAFKA_BOOTSTRAP_SERVERS = config.get("kafka_bootstrap_servers", "")
SPARK_VERSION = config.get("spark_version", "")
SENDER_ADDRESS=config.get("sender_address")
PASSWORD=config.get("password")
MONGO_DB_NAME=config.get("mongo_db_name")
MONGO_DB_URI=config.get("mongo_db_uri")

# Existing config variables...

# Resolve the path to the 'src' directory
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

# Path to new_categories.json
CATEGORIES_JSON_PATH = os.path.join(SRC_PATH, 'models', 'news_categorization_model', 'new_categories.json')
NEWS_TOPIC_MODEL_PATH = os.path.join(SRC_PATH, 'models', 'news_topic_model')
NEWS_CATEGORISATION_MODEL_PATH = os.path.join(SRC_PATH, 'models', 'news_categorization_model')

from pathlib import Path

def get_project_root():
    return Path(__file__).parent.parent.resolve()

# Paths
PROJECT_ROOT = get_project_root()
SRC_PATH = PROJECT_ROOT / 'src'
CATEGORIES_JSON_PATH = SRC_PATH / 'models/news_categorization_model/new_categories.json'
CHECKPOINT_DIR = PROJECT_ROOT / 'checkpoint'
FILTERED_RAW_NEWS_CHECKPOINT = CHECKPOINT_DIR / 'filtered_raw_news'
GENERAL_CHECKPOINT = CHECKPOINT_DIR / 'general'

if __name__=='__main__':

    print("Loaded configurations:")
    print(f"NEWSAPI_KEYS: {NEWSAPI_KEYS}")
    print(f"NEWSDATAAPI_KEY: {NEWSDATAAPI_KEY}")
    print(f"LANGUAGES: {LANGUAGES}")
    print(f"PAGE_SIZE: {PAGE_SIZE}")
    print(f"HOURS_PERIOD: {HOURS_PERIOD}")
    print(f"QUERY: {QUERY}")
    print(f"PAGE: {PAGE}")
    print(f"RAW_NEWS_TOPIC: {RAW_NEWS_TOPIC}")
    print(f"FILTERED_NEWS_TOPIC: {FILTERED_NEWS_TOPIC}")
    print(f"PROCESSED_NEWS_TOPIC: {PROCESSED_NEWS_TOPIC}")
    print(f"INTERACTIONS_TOPIC: {INTERACTIONS_TOPIC}")
    print(f"NULL_REPLACEMENTS: {NULL_REPLACEMENTS}")
    print(f"KAFKA_BOOTSTRAP_SERVERS: {KAFKA_BOOTSTRAP_SERVERS}")
    print(f"SPARK_VERSION: {SPARK_VERSION}")
    print(f"SRC_PATH: {SRC_PATH}")
    print(f"CATEGORIES_JSON_PATH: {CATEGORIES_JSON_PATH}")
    print(f"NEWS_CATEGORISATION_MODEL_PATH: {NEWS_CATEGORISATION_MODEL_PATH}")
    print(f"NEWS_TOPIC_MODEL_PATH: {NEWS_TOPIC_MODEL_PATH}")



