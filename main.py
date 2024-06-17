"""from pathlib import Path
import sys

from config.config import (
    NEWSAPI_KEYS, NEWSDATAAPI_KEY, LANGUAGES, PAGE_SIZE, HOURS_PERIOD, QUERY,
    PAGE, RAW_NEWS_TOPIC, FILTERED_NEWS_TOPIC, PROCESSED_NEWS_TOPIC, 
    INTERACTIONS_TOPIC, NULL_REPLACEMENTS, KAFKA_BOOTSTRAP_SERVERS, SPARK_VERSION
)

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve() 
sys.path.append(str(src_path))

from src.consumers.filtered_news_consumer import persist_filtered_news
from src.producers.news_producer import NewsProducer
#from src.stream_processor.news_preprocessor import NewsPreprocessor
from src.stream_processor.raw_news_stream_processor import process_raw_news_stream

news_producer=NewsProducer(servers=KAFKA_BOOTSTRAP_SERVERS,
             api_key=NEWSAPI_KEYS[0],
             topic=RAW_NEWS_TOPIC,
             page=PAGE,
             page_size=PAGE_SIZE,
             null_replacements=NULL_REPLACEMENTS,
             languages=LANGUAGES,
             query=QUERY
             )



process_raw_news_stream(
    servers=KAFKA_BOOTSTRAP_SERVERS,
    raw_news_topic=RAW_NEWS_TOPIC,
    filtered_news_topic=FILTERED_NEWS_TOPIC,
    processed_news_topic=PROCESSED_NEWS_TOPIC,
)
news_producer.db_connection(db=0)
news_producer.run(source='google_news')

news_producer.db_connection(db=1)
news_producer.run(source='newsapi')
print('++++++++++++++++++')
#p
#persist_filtered_news(topics=[FILTERED_NEWS_TOPIC],servers=KAFKA_BOOTSTRAP_SERVERS)"""