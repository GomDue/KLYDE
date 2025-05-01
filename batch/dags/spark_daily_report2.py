import sys
import argparse
import os
import shutil
from datetime import datetime, timedelta

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, count, from_json, to_timestamp
from pyspark.sql.types import ArrayType, StringType
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def main(report_date_str):
    print(f"시작 날짜: {report_date_str}")
    
    # 폰트 설정 (기본 폰트)
    FONT_PATH = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    INPUT_PATH = "/opt/airflow/data/realtime/*.json"
    REALTIME_DIR = "/opt/airflow/data/realtime"
    ARCHIVE_DIR = "/opt/airflow/data/news_archive"
    REPORT_DIR = "/opt/airflow/data"
    font_prop = fm.FontProperties(fname=FONT_PATH, size=12)
    

    spark = SparkSession.builder \
            .appName("DailyNewsReport") \
            .getOrCreate()
    
    # TODO: 데이터 처리, 리포트 저장, realtime 파일 -> news_archive로 이동 등


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spark를 이용한 일일 뉴스 리포트 생성")
    parser.add_argument("--date", required=True, help="보고서 기준 날짜 (YYYY-MM-DD)")
    args = parser.parse_args()

    main(args.date)


'''
airflow/
├── dags/
│   └── scripts/
│       └── spark_daily_report.py     ← 이 파일 위치
├── data/                            ← PDF 리포트 저장
│   ├── realtime/                     ← JSON 원본 데이터
│   └── news_archive/                ← 처리 완료된 파일 이동                       


mkdir -p dags/scripts         # Spark 스크립트
mkdir -p data/realtime        # JSON 수신
mkdir -p data/news_archive    # 이동 대상
mkdir -p data              # PDF 출력

'''
