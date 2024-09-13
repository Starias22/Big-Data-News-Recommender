from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from datetime import timedelta

import sys
from pathlib import Path

import pendulum
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))

from config.config import SRC_PATH,START_HOUR,START_DAYS_AGO,ADMIN_EMAIL, SPARK_CONNECTION_ID

from src.airflow_email import success_email,failure_email


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': pendulum.today('UTC').subtract(days=START_DAYS_AGO).replace(hour=START_HOUR+2),
    'email_on_failure': True,
    'email_on_success': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=15),
    'email':ADMIN_EMAIL
}



dag = DAG(
    'interactions_storage_dag',
    default_args=default_args,
    description='A daily dag for storage of user interactions with the news articles.' ,
    schedule_interval=timedelta(days=1),
    catchup = False,
)


interactions_storage_task = SparkSubmitOperator(
    task_id='interactions_storage',
    conn_id=SPARK_CONNECTION_ID,
    application=f'{SRC_PATH}/consumers/interactions_saver.py',
    dag=dag,
    #packages=SPARK_KAFKA_PACKAGES,
    deploy_mode="client",
    on_success_callback = success_email,
    on_failure_callback = failure_email,
)

