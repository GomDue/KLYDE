import logging
import pendulum
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.elasticsearch.hooks.elasticsearch import ElasticsearchPythonHook

log = logging.getLogger("daily-report")
local_tz = pendulum.timezone("Asia/Seoul")


def fetch_updated_data_from_postgres(last_run_time: datetime | None = None):
    """
    Postgres에서 특정 시각 이후에(updated > last_run_time) 수정된 뉴스 행을 가져옴

    Args:
        last_run_time: 이 시각 이후에 변경된 행만 조회, None이면 1970-01-01 00:00:00

    Returns:
        list[tuple]: (id, title, content, updated) 형태의 튜플 목록
    """
    if last_run_time is None:
        last_run_time = datetime(1970, 1, 1)

    postgres_hook = PostgresHook(postgres_conn_id="postgres_news")

    sql = """
        SELECT id, title, content, updated
        FROM news_article
        WHERE updated > %s
    """
    rows = postgres_hook.get_records(sql=sql, parameters=(last_run_time,))
    return rows


def sync_data_to_elasticsearch(updated_data: list[tuple]):
    """
    변경된 데이터를 Elasticsearch에 upsert

    동작 순서:
    1) 인덱스가 없으면 생성 시도(이미 있으면 무시)
    2) 각 레코드를 doc_as_upsert=True로 업데이트

    Args:
        updated_data: (id, title, content, updated) 형태의 튜플 목록

    Returns:
        None
    """
    if not updated_data:
        log.info("No new data to update in Elasticsearch.")
        return

    es_hook = ElasticsearchPythonHook(elasticsearch_conn_id="elasticsearch_connection")
    es_client = es_hook.get_conn()
    index_name = "news"

    try:
        es_client.indices.create(index=index_name)
        log.info("Created index: %s", index_name)
    except Exception:
        pass

    success = 0
    for record in updated_data:
        doc_id = record[0]
        document = {
            "title":      record[1],
            "content":    record[2],
            "updated_at": record[3],
        }
        es_client.update(index=index_name, id=doc_id, doc=document, doc_as_upsert=True)
        success += 1

    log.info("ES upsert done: docs=%d", success)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
with DAG(
    dag_id="sync_postgres_to_elasticsearch",
    default_args=default_args,
    description="Synchronize PostgreSQL and Elasticsearch every 10 minutes",
    schedule_interval=timedelta(minutes=10),
    start_date=datetime(2025, 5, 1, tzinfo=local_tz),
    catchup=False,
    tags=["sync", "postgres", "elasticsearch"],
) as dag:

    def fetch_updated_data_task(**context):
        last_run_time = context.get("data_interval_start") or datetime(1970, 1, 1)
        log.info("Fetch window start=%s", last_run_time)

        updated_data = fetch_updated_data_from_postgres(last_run_time)
        context["ti"].xcom_push(key="updated_data", value=updated_data)

    def sync_data_to_elasticsearch_task(**context):
        rows = context["ti"].xcom_pull(
            task_ids="fetch_updated_data_task", key="updated_data"
        )
        log.info("Start ES upsert: rows=%d", len(rows))
        sync_data_to_elasticsearch(rows)

    fetch_task = PythonOperator(
        task_id="fetch_updated_data_task",
        python_callable=fetch_updated_data_task
    )

    sync_task = PythonOperator(
        task_id="sync_data_to_elasticsearch_task",
        python_callable=sync_data_to_elasticsearch_task
    )

    fetch_task >> sync_task
