from airflow import DAG
from airflow.operators.bash_operator import BashOperator # type: ignore
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
import sys
from pathlib import Path
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))

from config.config import START_HOUR,START_DAYS_AGO
from src.utils import increment_hour


CONSUMERS_PATH='~/Big-Data-News-Recommender/src/consumers/'
STREAM_PROCESSOR_PATH='~/Big-Data-News-Recommender/src/stream_processors/'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    #'start_date': datetime(2024, 6, 23,hour= 6, minute=15),
    'start_date': days_ago(START_DAYS_AGO,hour=START_HOUR+3),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=10),
}


dag = DAG(
    'news_recommendation_dag',
    default_args=default_args,
    description='A daily dag for retrieving available news and generating news recommendations.' ,
    #schedule_interval=timedelta(hours=1),
    schedule_interval=timedelta(days=1),
)




available_news_fetching_task = BashOperator(
    task_id='available_news_fetching',
    bash_command=f'python3 {STREAM_PROCESSOR_PATH}processed_news_forwarder.py',
    dag=dag,
)
available_news_recommendation_task = BashOperator(
    task_id='available_news_recommending',
    bash_command=f'python3 {CONSUMERS_PATH}available_news_recommender.py',
    dag=dag,
)


available_news_fetching_task>>available_news_recommendation_task
