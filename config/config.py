import json
import os
from pathlib import Path


START_HOUR=2
#START_HOUR=8
START_DAYS_AGO=1
def load_config(filepath='secret.json'):
    # Use absolute path to ensure we find the file
    abs_filepath = os.path.join(os.path.dirname(__file__), filepath)
    with open(abs_filepath, 'r') as file:
        return json.load(file)
# Load configurations from config.json


config = load_config()

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

KAFKA_BOOTSTRAP_SERVERS=os.getenv("KAFKA_BOOTSTRAP_SERVERS","localhost:9092,localhost:9093,localhost:9094")

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


def get_project_root():
    return Path(__file__).parent.parent.resolve()

# Paths
PROJECT_ROOT = get_project_root()
SRC_PATH = PROJECT_ROOT / 'src'

# Resolve the path to the 'src' directory
path = PROJECT_ROOT / 'src'
SRC_PATH=str(os.getenv("SRC_PATH",path))

"""print('*************************')
print(SRC_PATH)
print(type(SRC_PATH))"""
#os.environ.pop('TRAINED_MODELS_PATH', None)
TRAINED_MODELS_PATH=os.getenv("TRAINED_MODELS_PATH",PROJECT_ROOT/'trained_models')
print(TRAINED_MODELS_PATH)
# Path to new_categories.json
NEWS_CATEGORISATION_MODEL_PATH = os.path.join(TRAINED_MODELS_PATH, 'news_categorization_model')

CATEGORIES_JSON_PATH = os.path.join(NEWS_CATEGORISATION_MODEL_PATH, 'news_categories.json')

CHECKPOINT_DIR=os.getenv("CHECKPOINT_DIR",str(PROJECT_ROOT/'checkpoint-local/'))

# Load category mapping and config
with open(CATEGORIES_JSON_PATH, 'r') as f:
    category_mapping = json.load(f)

# Convert keys to integers for category mapping
CATEGORIES_MAPPING = {int(k): v for k, v in category_mapping.items()}

#print(CHECKPOINT_DIR)

KAFKA_JARS= [
    '/opt/bitnami/spark/jars/spark-sql-kafka-0-10_2.12-3.5.1.jar',
    '/opt/bitnami/spark/jars/spark-streaming-kafka-0-10_2.12-3.5.1.jar',
    '/opt/bitnami/spark/jars/spark-token-provider-kafka-0-10_2.12-3.5.1.jar'
]
KAFKA_PACKAGES="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.5.1"


FILTERED_NEWS_CHECKPOINT_DIR = CHECKPOINT_DIR +'/filtered_news/'
AVAILABLE_NEWS_CHECKPOINT_DIR = CHECKPOINT_DIR+ '/available_news/'
AVAILABLE_NEWS_RECOMMENDER_CHECKPOINT_DIR = SRC_PATH +'/consumer/checkpoint/recommender'
PROCESSED_NEWS_CHECKPOINT_DIR = CHECKPOINT_DIR + '/processed_news/'
SPARK_STREAM_CHECKPOINT_LOCATION=PROJECT_ROOT / 'src/processors/checkpoint/'
NLTK_DATA_PATH=str(PROJECT_ROOT)+'/nltk_data'



if __name__=='__main__':
    print('+++++++++++++++++++++++++++++')
    print("Loaded configurations:")
    print(f"NEWSAPI_KEYS: {NEWSAPI_KEYS}")
    #print(f"NEWSDATAAPI_KEY: {NEWSDATAAPI_KEY}")
    print(f"LANGUAGES: {LANGUAGES}")
    print(f"PAGE_SIZE: {PAGE_SIZE}")
    print(f"HOURS_PERIOD: {HOURS_PERIOD}")
    print(f"QUERY: {QUERY}")
    print(f"PAGE: {PAGE}")
    print(f"RAW_NEWS_TOPIC: {RAW_NEWS_TOPIC}")
    print(f"FILTERED_NEWS_TOPIC: {FILTERED_NEWS_TOPIC}")
    print(f"PROCESSED_NEWS_TOPIC: {PROCESSED_NEWS_TOPIC}")
    print(f"AVAILABLE_NEWS_TOPIC: {AVAILABLE_NEWS_TOPIC}")
    print(f"INTERACTIONS_TOPIC: {INTERACTIONS_TOPIC}")
    print(f"NULL_REPLACEMENTS: {NULL_REPLACEMENTS}")
    print(f"KAFKA_BOOTSTRAP_SERVERS: {KAFKA_BOOTSTRAP_SERVERS}")
    print(f"SPARK_VERSION: {SPARK_VERSION}")
    print(f"SRC_PATH: {SRC_PATH}")
    print(f"CATEGORIES_JSON_PATH: {CATEGORIES_JSON_PATH}")
    print(f"NEWS_CATEGORISATION_MODEL_PATH: {NEWS_CATEGORISATION_MODEL_PATH}")




