
from airflow import DAG
from airflow.operators.bash import BashOperator 
from datetime import timedelta
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

import sys
from pathlib import Path

import pendulum
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))

from config.config import START_HOUR,START_DAYS_AGO,SRC_PATH,KAFKA_PACKAGES,ADMIN_EMAIL
from src.airflow_email import success_email,failure_email





default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': pendulum.today('UTC').add(days=-START_DAYS_AGO).replace(hour=START_HOUR+1),
    'email_on_failure': True,
    'email_on_success': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=15),
    'email':ADMIN_EMAIL,
}


dag = DAG(
    'news_etl_dag',
    default_args=default_args,
    description='A daily workflow for processing news in realtime.' 
    +'It includes fetching news from RawNewsTopic, filtering news and sending them' 
    +'to FilteredNewsTopic, processing news and sending them to ProcessdeNewsTopic and also stroreg'
    +' of processed news',
    schedule_interval=timedelta(days=1),
    catchup = False,
)


raw_news_stream_processing_task = SparkSubmitOperator(
    task_id='raw_news_stream_processing',
    conn_id='spark-connection',
    application=f'{SRC_PATH}/stream_processors/raw_news_stream_processor.py',
    dag=dag,
    packages=KAFKA_PACKAGES,
    deploy_mode="client",
    on_success_callback = success_email,
     on_failure_callback = failure_email,
)


filtered_news_storage_task = BashOperator(
    task_id='filtered_news_storage',
    bash_command=f'python3 {SRC_PATH}/consumers/filtered_news_saver.py',
    dag=dag,
    on_success_callback = success_email,
     on_failure_callback = failure_email,
)
raw_news_stream_processing_task>>filtered_news_storage_task
