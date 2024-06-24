from airflow import DAG
from airflow.operators.bash_operator import BashOperator # type: ignore
from datetime import datetime, timedelta
CONSUMERS_PATH='~/Big-Data-News-Recommender/src/consumers/'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 23,hour= 2, minute=0),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=10),
}


dag = DAG(
    'final_dag',
    default_args=default_args,
    description='A daily dag for saving filtered news, generating news recommendations.' 
    +'and storage of user interactions with the news articles.',
    #schedule_interval=timedelta(hours=1),
    schedule_interval=timedelta(days=1),
)



filtered_news_storage_task = BashOperator(
    task_id='filtered_news_storage',
    bash_command=f'python3 {CONSUMERS_PATH}filtered_news_saver.py',
    dag=dag,
)
available_news_recommending_task = BashOperator(
    task_id='available_news_recommending',
    bash_command=f'python3 {CONSUMERS_PATH}available_news_recommender.py',
    dag=dag,
)


interactions_storage_task = BashOperator(
    task_id='interactions_storage',
    bash_command=f'python3 {CONSUMERS_PATH}interactions_saver.py',
    dag=dag,
)
