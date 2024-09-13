from airflow import DAG
from datetime import timedelta
import sys
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from pathlib import Path

import pendulum
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))

from config.config import START_HOUR,START_DAYS_AGO,SRC_PATH,SPARK_KAFKA_PACKAGES,ADMIN_EMAIL, SPARK_CONNECTION_ID

from src.airflow_email import success_email,failure_email

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': pendulum.today('UTC').subtract(days=START_DAYS_AGO).replace(hour=START_HOUR+3),
    'email_on_failure': True,
    'email_on_success': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=15),
    'email':ADMIN_EMAIL
}


dag = DAG(
    'news_recommendation_dag',
    default_args=default_args,
    description='A daily dag for retrieving available news and generating news recommendations.',
    schedule_interval=timedelta(days=1),
    catchup = False,
)

available_news_fetching_task = SparkSubmitOperator(
    task_id='available_news_fetching',
    conn_id=SPARK_CONNECTION_ID,
    application=f'{SRC_PATH}/processors/processed_news_forwarder.py',
    dag=dag,
    packages=SPARK_KAFKA_PACKAGES,
    deploy_mode="client",
    on_success_callback = success_email,
     on_failure_callback = failure_email,
)

available_news_recommendation_task = SparkSubmitOperator(
    task_id='available_news_recommending',
    conn_id=SPARK_CONNECTION_ID,
    application=f'{SRC_PATH}/consumers/available_news_recommender.py',
    dag=dag,
    packages=SPARK_KAFKA_PACKAGES,
    deploy_mode="client",
    on_success_callback = success_email,
     on_failure_callback = failure_email,
)

available_news_fetching_task >> available_news_recommendation_task
