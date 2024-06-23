from airflow import DAG
from airflow.operators.bash_operator import BashOperator # type: ignore
from datetime import datetime, timedelta
PRODUCERS_PATH='~/Big-Data-News-Recommender/src/producers/'
STREAM_PROCESSOR_PATH='~/Big-Data-News-Recommender/src/stream_processors/'
CONSUMERS_PATH='~/Big-Data-News-Recommender/src/consumers/'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 22,hour=23,minute=00),
    'email_on_failure': 'bdnews.recommend@gmail.com',
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=10),
}


dag = DAG(
    'bdnews_workflow_dag',
    default_args=default_args,
    description='A daily workflow for processing and recommending news articles. '
    +'This DAG includes tasks for producing raw news data from multiple sources,' 
    +'processing this data, saving filtered news, and generating recommendations.' 
    +'Additionally, it handles the storage of user interactions with the news articles.',
    schedule_interval=timedelta(hours=1),
    #schedule_interval='@daily',
)

news_api_producer_task = BashOperator(
    task_id='news_api_producer',
    bash_command=f'python3 {PRODUCERS_PATH}news_api_producer.py',
    dag=dag,
)
google_news_producer_task = BashOperator(
    task_id='google_news_producer',
    bash_command=f'python3 {PRODUCERS_PATH}google_news_producer.py',
    dag=dag,
)
raw_news_processor_task = BashOperator(
    task_id='raw_news_stream_processor',
    bash_command=f'python3 {STREAM_PROCESSOR_PATH}raw_news_stream_processor.py',
    dag=dag,
)

filtered_news_saver_task = BashOperator(
    task_id='filtered_news_saver',
    bash_command=f'python3 {CONSUMERS_PATH}filtered_news_saver.py',
    dag=dag,
)
processed_news_recommender_task = BashOperator(
    task_id='processed_news_recommender',
    bash_command=f'python3 {CONSUMERS_PATH}processed_news_recommender.py',
    dag=dag,
)


interactions_saver_task = BashOperator(
    task_id='interactions_saver',
    bash_command=f'python3 {CONSUMERS_PATH}interactions_saver.py',
    dag=dag,
)

[news_api_producer_task ,google_news_producer_task ]>>raw_news_processor_task >> [filtered_news_saver_task,processed_news_recommender_task]
