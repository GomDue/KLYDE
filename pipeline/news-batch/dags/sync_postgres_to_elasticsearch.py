import pendulum
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
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
    if last_run_time is None:
        last_run_time = datetime(1970, 1, 1)

    postgres_hook = PostgresHook(postgres_conn_id="postgres_news")

    sql = f"""
        SELECT * FROM news_article
        WHERE updated > '{last_run_time}'
    """
    
    updated_data = postgres_hook.get_records(sql)
    return updated_data

def sync_data_to_elasticsearch(updated_data):
    """
    Sync updated data from PostgreSQL to Elasticsearch using ElasticsearchHook.
    """
    if not updated_data:
        print("[INFO] No new data to update in Elasticsearch.")
        return

    es_hook = ElasticsearchHook(elasticsearch_conn_id="elasticsearch_connection")
    es_client = es_hook.get_conn()
    index_name = "news"
    
    for record in updated_data:
        doc_id = record[0]
        document = {
            "title": record[1],
            "content": record[2],
            "updated_at": record[3],
        }
        es_client.update(index=index_name, id=doc_id, body={"doc": document, "doc_as_upsert": True})
    
    print(f"[INFO] Updated {len(updated_data)} documents in Elasticsearch.")

with DAG(
    dag_id='sync_postgres_to_elasticsearch',
    default_args=default_args,
    description='Synchronize PostgreSQL and Elasticsearch every 10 minutes',
    schedule_interval=timedelta(minutes=10),
    start_date=datetime(2025, 5, 1, tzinfo=local_tz),
    catchup=False,
    tags=['sync', 'postgres', 'elasticsearch'],
) as dag:

    def fetch_updated_data_task(**context):
        # Use data_interval_start as the last_run_time
        last_run_time = context.get('data_interval_start') or datetime(1970, 1, 1)
        print(f"[INFO] Last run time: {last_run_time}")

        updated_data = fetch_updated_data_from_postgres(last_run_time)
        context['ti'].xcom_push(key='updated_data', value=updated_data)

    def sync_data_to_elasticsearch_task(**context):
        updated_data = context['ti'].xcom_pull(task_ids='fetch_updated_data_task', key='updated_data')
        sync_data_to_elasticsearch(updated_data)

    fetch_task = PythonOperator(
        task_id='fetch_updated_data_task',
        python_callable=fetch_updated_data_task,
    )

    sync_task = PythonOperator(
        task_id='sync_data_to_elasticsearch_task',
        python_callable=sync_data_to_elasticsearch_task,
    )

    fetch_task >> sync_task
