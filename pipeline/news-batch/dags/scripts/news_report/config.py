import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pendulum

DOTENV_PATH = "/opt/airflow/.env"
load_dotenv(dotenv_path=DOTENV_PATH)


KST = pendulum.timezone("Asia/Seoul")

def dates_kst_now():
    report_dt = datetime.now(tz=KST)
    yester_dt = report_dt - timedelta(days=1)
    return report_dt, yester_dt

def date_strings(report_dt, yester_dt):
    yester_date_str = yester_dt.strftime("%Y-%m-%d")
    yester_start_ts = f"{yester_date_str} 00:00:00"
    yester_end_ts   = f"{yester_date_str} 23:59:59"
    report_date_str = report_dt.strftime("%Y%m%d")
    return report_date_str, yester_date_str, yester_start_ts, yester_end_ts


# PostgreSQL
POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT")
POSTGRESQL_DB   = os.getenv("POSTGRESQL_DB")
POSTGRESQL_USER = os.getenv("POSTGRESQL_USER")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
POSTGRESQL_URL = os.getenv("POSTGRESQL_URL")

JDBC_DRIVER = "org.postgresql.Driver"


# Paths
FONT_PATH  = os.getenv("FONT_PATH")
REPORT_DIR = os.getenv("REPORT_DIR")

# Tables
ARTICLES_TABLE    = os.getenv("ARTICLES_TABLE")
DM_KEYWORDS_TABLE = os.getenv("DM_KEYWORDS_TABLE")
DM_CATEGORY_TABLE = os.getenv("DM_CATEGORY_TABLE")
DM_SUMMARY_TABLE  = os.getenv("DM_SUMMARY_TABLE")
