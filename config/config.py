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
