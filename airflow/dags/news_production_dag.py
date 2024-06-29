from pathlib import Path
from airflow import DAG
from airflow.operators.bash_operator import BashOperator # type: ignore
from datetime import timedelta
from airflow.utils.dates import days_ago
import sys
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))


from config.config import START_HOUR,START_DAYS_AGO


PRODUCERS_PATH='~/Big-Data-News-Recommender/src/producers/'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    #'start_date': datetime(2024, 6, 23,hour= 4, minute=15),
    'start_date': days_ago(START_DAYS_AGO,hour=START_HOUR),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=10),
}


dag = DAG(
    'news_production_dag',
    default_args=default_args,
    description='A daily workflow for fetching news articles from multiples sources.',
    #schedule_interval=timedelta(hours=1),
    schedule_interval=timedelta(days=1),
)

news_api_production_task = BashOperator(
    task_id='news_api_production',
    bash_command=f'python3 {PRODUCERS_PATH}news_api_producer.py',
    dag=dag,
)
google_news_production_task = BashOperator(
    task_id='google_news_production',
    bash_command=f'python3 {PRODUCERS_PATH}google_news_producer.py',
    dag=dag,
)
