from airflow import DAG
from airflow.operators.bash_operator import BashOperator # type: ignore
from datetime import datetime, timedelta
PRODUCERS_PATH='~/Big-Data-News-Recommender/src/producers/'
STREAM_PROCESSOR_PATH='~/Big-Data-News-Recommender/src/stream_processors/'
CONSUMERS_PATH='~/Big-Data-News-Recommender/src/consumers/'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 23,hour= 1, minute=0),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=10),
}


dag = DAG(
    'raw_news_stream_processing_dag',
    default_args=default_args,
    description='A daily workflow for processing news in realtime.' 
    +'It includes fetching news from RawNewsTopic, filtering news and sending them' 
    +'to FilteredNewsTopic, and then processing news and sending them to ProcessdeNewsTopic',
    #schedule_interval=timedelta(hours=1),
    schedule_interval=timedelta(days=1),
)

raw_news_stream_processing_task = BashOperator(
    task_id='raw_news_stream_processing',
    bash_command=f'python3 {STREAM_PROCESSOR_PATH}raw_news_stream_processor.py',
    dag=dag,
)

