"""This is the module for news production DAG"""
import sys
from pathlib import Path
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))

from config.config import SRC_PATH,START_HOUR,START_DAYS_AGO,ADMIN_EMAIL
from src.airflow_email import success_email,failure_email

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': pendulum.today('UTC').subtract(days=START_DAYS_AGO).replace(hour=START_HOUR),
    'email_on_failure': True,
    'email_on_success': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=15),
    'email':ADMIN_EMAIL
}

dag = DAG(
    'news_production_dag',
    default_args=default_args,
    description='A daily workflow for fetching news articles from multiples sources.',
    schedule=timedelta(days=1),
    catchup = False,
)

news_api_production_task = BashOperator(
    task_id='news_api_production',
    bash_command=f'python3 {SRC_PATH}/producers/news_api_producer.py',
    dag=dag,
    on_success_callback = success_email,
    on_failure_callback = failure_email,
)
google_news_production_task = BashOperator(
    task_id='google_news_production',
    bash_command=f'python3 {SRC_PATH}/producers/google_news_producer.py',
     on_success_callback = success_email,
     on_failure_callback = failure_email,
    dag=dag,

)
