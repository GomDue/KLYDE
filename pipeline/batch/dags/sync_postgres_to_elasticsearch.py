import pendulum
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.elasticsearch.hooks.elasticsearch import ElasticsearchHook

local_tz = pendulum.timezone("Asia/Seoul")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_updated_data_from_postgres(last_run_time=None):
    """
    Fetch updated data from PostgreSQL where updated_at is greater than last_run_time.
    """
    if last_run_time is None:
        last_run_time = datetime(1970, 1, 1)  # Default to a very old date
    
    # Connect to PostgreSQL using PostgresHook
    postgres_hook = PostgresHook(postgres_conn_id="postgres_news")
    
    # SQL query to fetch updated rows
    sql = f"""
    SELECT * FROM your_table
    WHERE updated_at > '{last_run_time}'
    """
    
    # Fetch data
    updated_data = postgres_hook.get_records(sql)
    return updated_data

def sync_data_to_elasticsearch(updated_data):
    """
    Sync updated data from PostgreSQL to Elasticsearch using ElasticsearchHook.
    """
    if not updated_data:
        print("No new data to update in Elasticsearch.")
        return
    
    # Connect to Elasticsearch using ElasticsearchHook
    es_hook = ElasticsearchHook(elasticsearch_conn_id="elasticsearch_connection")
    es_client = es_hook.get_conn()
    index_name = "news"
    
    # Process each record and update Elasticsearch
    for record in updated_data:
        doc_id = record[0]  # Assuming the first column is the ID
        document = {
            "title": record[1],  # Assuming the second column is title
            "content": record[2],  # Assuming the third column is content
            "updated_at": record[3],  # Assuming the fourth column is updated_at
        }
        es_client.update(index=index_name, id=doc_id, body={"doc": document, "doc_as_upsert": True})
    print(f"Updated {len(updated_data)} documents in Elasticsearch.")

with DAG(
    dag_id='sync_postgres_to_elasticsearch',
    default_args=default_args,
    description='Synchronize PostgreSQL and Elasticsearch every 10 minutes',
    schedule_interval=timedelta(minutes=10),
    start_date=datetime(2025, 5, 1, tzinfo=local_tz),
    catchup=False,
    tags=['sync', 'postgres', 'elasticsearch']
) as dag:

    def fetch_updated_data_task(**kwargs):
        last_run_time = kwargs['previous_execution_date'] or datetime(1970, 1, 1)
        updated_data = fetch_updated_data_from_postgres(last_run_time)
        kwargs['ti'].xcom_push(key='updated_data', value=updated_data)

    def sync_data_to_elasticsearch_task(**kwargs):
        updated_data = kwargs['ti'].xcom_pull(task_ids='fetch_updated_data_task', key='updated_data')
        sync_data_to_elasticsearch(updated_data)

    fetch_updated_data_task = PythonOperator(
        task_id='fetch_updated_data_task',
        python_callable=fetch_updated_data_task,
        provide_context=True,
        dag=dag,
    )

    sync_data_to_elasticsearch_task = PythonOperator(
        task_id='sync_data_to_elasticsearch_task',
        python_callable=sync_data_to_elasticsearch_task,
        provide_context=True,
        dag=dag,
    )

    fetch_updated_data_task >> sync_data_to_elasticsearch_task
