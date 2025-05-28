import pendulum
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

local_tz = pendulum.timezone("Asia/Seoul")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='daily_report_dag',
    default_args=default_args,
    description='매일 새벽 1시에 Spark를 이용해 뉴스 리포트 생성',
    schedule_interval='0 1 * * *',
    start_date=datetime(2025, 5, 1, tzinfo=local_tz), 
    catchup=False,
    tags=['daily', 'report', 'spark']
) as dag:
    
    submit_spark_job = SparkSubmitOperator(
        task_id='spark_daily_report',
        application='/opt/airflow/dags/scripts/spark_daily_report.py',
        conn_id='spark_default',
        conf={'spark.submit.deployMode': 'client'},
    )

    notify_report_generated = BashOperator(
        task_id='notify_report_generated',
        bash_command=(
            'echo "리포트가 생성되었습니다: {{ execution_date.strftime("%Y-%m-%d") }} 날짜의 이메일 보내기"'
        )
    )
    
    send_report_email = EmailOperator(
        task_id='send_report_email',
        to='ghdtmddid@gmail.com',
        subject='[뉴스 리포트] {{ execution_date.strftime("%Y-%m-%d") }} 기준 키워드 분석 결과',
        html_content=""" 
            <p>안녕하세요,</p>
            <p>{{ execution_date.strftime("%Y-%m-%d") }} 기준 뉴스 리포트가 생성되었습니다.</p>
            <p>첨부된 PDF 파일을 확인해주세요.</p>
        """,
        files=["/opt/airflow/data/daily_report_{{ execution_date.strftime('%Y%m%d') }}.pdf"],
    )

    submit_spark_job >> notify_report_generated >> send_report_email
