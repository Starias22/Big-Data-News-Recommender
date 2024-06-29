
from airflow import DAG
from airflow.operators.bash_operator import BashOperator # type: ignore
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
import sys
from pathlib import Path
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))

from config.config import START_HOUR

PRODUCERS_PATH='~/Big-Data-News-Recommender/src/producers/'
STREAM_PROCESSOR_PATH='~/Big-Data-News-Recommender/src/stream_processors/'
CONSUMERS_PATH='~/Big-Data-News-Recommender/src/consumers/'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    #'start_date': datetime(2024, 6, 23,hour= 5, minute=15),
    'start_date': days_ago(1,hour=START_HOUR+1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=10),
}


dag = DAG(
    'news_etl_dag',
    default_args=default_args,
    description='A daily workflow for processing news in realtime.' 
    +'It includes fetching news from RawNewsTopic, filtering news and sending them' 
    +'to FilteredNewsTopic, processing news and sending them to ProcessdeNewsTopic and also stroreg'
    +' of processed news',
    #schedule_interval=timedelta(hours=1),
    schedule_interval=timedelta(days=1),
)

raw_news_stream_processing_task = BashOperator(
    task_id='raw_news_stream_processing',
    bash_command=f'python3 {STREAM_PROCESSOR_PATH}raw_news_stream_processor.py',
    dag=dag,
)

filted_news_storage_task = BashOperator(
    task_id='filted_news_storage',
    bash_command=f'python3 {CONSUMERS_PATH}filtered_news_saver.py',
    dag=dag,
)
raw_news_stream_processing_task>>filted_news_storage_task

