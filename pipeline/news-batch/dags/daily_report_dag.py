import logging
import pendulum
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.email import send_email


log = logging.getLogger("daily-report")
local_tz = pendulum.timezone("Asia/Seoul")


def fetch_email_recipients(**context):
    """
    email_consent=True 인 사용자 이메일 목록을 Postgres에서 가져옴

    동작 순서:
    1) PostgresHook으로 DB 접속
    2) "email_consent = TRUE" 인 email 목록 조회
    3) 조회 결과를 XCom("recipients")으로 푸시

    XCom Keys:
        - recipients: ["a@b.com", "c@d.com", ...]
    """
    postgres_hook = PostgresHook(postgres_conn_id="postgres_news")

    sql = f"""
        SELECT email
        FROM users_user
        WHERE email_consent = TRUE
          AND email IS NOT NULL
    """
    rows = postgres_hook.get_records(sql=sql)
    recipients = [r[0] for r in rows]
    log.info("Consenting recipients fetched: count=%d", len(recipients))
    context["ti"].xcom_push(key="recipients", value=recipients)


def send_report_email_task(**context):
    """
    XCom에서 수신자 목록을 꺼내 리포트 이메일을 발송합니다.

    동작 순서:
    1) XCom에서 recipients 가져오기
    2) 제목/본문/첨부파일 경로 구성
    3) send_email()로 전송
    """
    recipients = context["ti"].xcom_pull(task_ids="fetch_email_recipients", key="recipients")
    if not recipients:
        log.info("No consenting recipients found; skip sending email.")
        return

    ds = context["ds"] 
    ds_nodash = context["ds_nodash"]

    subject = f"[뉴스 리포트] {ds} 기준 분석 결과"
    html_content = (
        "<p>안녕하세요,</p>"
        f"<p>{ds} 기준 뉴스 리포트가 생성되었습니다.</p>"
        "<p>첨부된 PDF 파일을 확인해주세요.</p>"
    )
    files = [f"/opt/airflow/data/news_summary/daily_report_{ds_nodash}.pdf"]

    send_email(to=recipients, subject=subject, html_content=html_content, files=files)
    log.info("Email sent: to=%d recipients attach=%s", len(recipients), files[0])


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
with DAG(
    dag_id="daily_report_dag",
    default_args=default_args,
    description="매일 새벽 1시에 Spark를 이용해 뉴스 리포트 생성",
    schedule_interval="0 1 * * *",
    start_date=datetime(2025, 5, 1, tzinfo=local_tz),
    catchup=False,
    tags=["daily", "report", "spark"]
) as dag:
    
    submit_spark_job = SparkSubmitOperator(
        task_id="spark_daily_report",
        application="/opt/airflow/dags/scripts/news_report/daily_report.py",
        conn_id="spark_default",
        conf={"spark.submit.deployMode": "cluster"}, # Spark Cluster에서 실행
        packages="org.postgresql:postgresql:42.7.3",
        env_vars={"DOTENV_PATH": "/opt/airflow/.env"},
    )

    notify_report_generated = BashOperator(
        task_id="notify_report_generated",
        bash_command='echo "리포트 생성됨: {{ ds }} 이메일 전송 준비"'
    )

    fetch_recipients = PythonOperator(
        task_id="fetch_email_recipients",
        python_callable=fetch_email_recipients
    )

    send_report_email = PythonOperator(
        task_id="send_report_email",
        python_callable=send_report_email_task
    )

    submit_spark_job >> notify_report_generated >> fetch_recipients >> send_report_email

