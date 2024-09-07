"""This module defines configuration variables"""
import json
import os
from pathlib import Path

START_HOUR=2
START_DAYS_AGO=0

# Load configurations from config.json
# Use absolute path to ensure we find the file
abs_filepath = os.path.join(os.path.dirname(__file__), 'secret.json')
with open(abs_filepath, 'r', encoding='utf-8') as file:
    config=json.load(file)

# Assign configurations to variables
NEWSAPI_KEYS = [
    config.get("newsapi_key", ""),
    config.get("newsapi_key2", ""),
    config.get("newsapi_key3", ""),
    config.get("newsapi_key4", ""),
    config.get("newsapi_key5", "")
]
#NEWSDATAAPI_KEY = config.get("newsdataapi_key", "")
LANGUAGES = ["en","fr","es"]
PAGE_SIZE = 100
HOURS_PERIOD = 25
QUERY = ["technology","finance","health","economy","war","business",
    "biology","science","politics","family","ecology","coronavirus","Gaza",
    "Israel","Palsestine","Ukraine","Benin","Niger","Morocco","sports","Trump",
    "Biden","education","crime","justice","religion","travel","weddings","styles","nation"
  ]
PAGE = 1 # Example default value
RAW_NEWS_TOPIC = "RawNewsTopic"
FILTERED_NEWS_TOPIC = "FilteredNewsTopic"
PROCESSED_NEWS_TOPIC = "ProcessedNewsTopic"
AVAILABLE_NEWS_TOPIC="AvailableNewsTopic"
INTERACTIONS_TOPIC = "InteractionsTopic"
NULL_REPLACEMENTS = {
        "":None,
        "[Removed]": None,  
        "https://removed.com": None
}

KAFKA_BOOTSTRAP_SERVERS=os.getenv("KAFKA_BOOTSTRAP_SERVERS","localhost:9092")
#KAFKA_BOOTSTRAP_SERVERS=os.getenv("KAFKA_BOOTSTRAP_SERVERS","localhost:9092,
# localhost:9093,localhost:9094")

SPARK_VERSION = "3.5.1"
SENDER_ADDRESS=config.get("sender_address")
PASSWORD=config.get("password")
ADMIN_EMAIL=config.get("admin_email")
MONGO_DB_NAME="news_recommendation_db"

#os.environ.pop('MONGO_DB_URI', None)
MONGO_DB_URI=os.getenv("MONGO_DB_URI","mongodb://localhost:27017/")
#print(888888888888888888888)
print(MONGO_DB_URI)
LOCALHOST="localhost"
REDIS_HOST=os.getenv("REDIS_HOST",LOCALHOST)
TIME_OUT_MS=1000
GROUP_TIME_OUT_MS=5000
DISLIKED=-1
SEEN=0
LIKED=1

POSITIVE_SENTIMENT=1
NEGATIVE_SENTIMENT=-1
NEUTRAL_SENTIMENT=0

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
SRC_PATH = PROJECT_ROOT / 'src'

# Resolve the path to the 'src' directory
path = PROJECT_ROOT / 'src'
SRC_PATH=str(os.getenv("SRC_PATH",path))

TRAINED_MODELS_PATH=os.getenv("TRAINED_MODELS_PATH",PROJECT_ROOT/'trained_models')
# Path to new_categories.json
NEWS_CATEGORISATION_MODEL_PATH = os.path.join(TRAINED_MODELS_PATH, 'news_categorization_model')

CATEGORIES_JSON_PATH = os.path.join(NEWS_CATEGORISATION_MODEL_PATH, 'news_categories.json')

CHECKPOINT_DIR=os.getenv("CHECKPOINT_DIR",str(PROJECT_ROOT/'checkpoint-local/'))

# Load category mapping and config
with open(CATEGORIES_JSON_PATH, 'r', encoding='utf-8') as f:
    category_mapping = json.load(f)

# Convert keys to integers for category mapping
CATEGORIES_MAPPING = {int(k): v for k, v in category_mapping.items()}

KAFKA_JARS= [
    '/opt/bitnami/spark/jars/spark-sql-kafka-0-10_2.12-3.5.1.jar',
    '/opt/bitnami/spark/jars/spark-streaming-kafka-0-10_2.12-3.5.1.jar',
    '/opt/bitnami/spark/jars/spark-token-provider-kafka-0-10_2.12-3.5.1.jar'
]
KAFKA_PACKAGES="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,\
org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.5.1"


FILTERED_NEWS_CHECKPOINT_DIR = CHECKPOINT_DIR +'/filtered_news/'
AVAILABLE_NEWS_CHECKPOINT_DIR = CHECKPOINT_DIR+ '/available_news/'
AVAILABLE_NEWS_RECOMMENDER_CHECKPOINT_DIR = SRC_PATH +'/consumer/checkpoint/recommender'
PROCESSED_NEWS_CHECKPOINT_DIR = CHECKPOINT_DIR + '/processed_news/'
SPARK_STREAM_CHECKPOINT_LOCATION=PROJECT_ROOT / 'src/processors/checkpoint/'
NLTK_DATA_PATH=str(PROJECT_ROOT)+'/nltk_data'
