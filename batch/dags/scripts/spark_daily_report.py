import sys
import argparse
import os
import shutil
from datetime import datetime, timedelta

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, udf
from pyspark.sql.types import ArrayType, StringType
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def main(report_date_str):
    print(f"[INFO] 리포트 기준 날짜: {report_date_str}")
    
    # 날짜 처리
    report_date = datetime.strptime(report_date_str, "%Y-%m-%d")
    yester_date = report_date - timedelta(days=1)

    yester_str = yester_date.strftime("%Y%m%d")
    report_str = report_date.strftime("%Y%m%d")
    yester_title_str = yester_date.strftime("%Y-%m-%d")

    # 경로 설정
    FONT_PATH = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    INPUT_PATH = f"/opt/airflow/data/realtime/{yester_str}.json"
    ARCHIVE_PATH = f"/opt/airflow/data/news_archive/{yester_str}.json"
    REPORT_PATH = f"/opt/airflow/data/daily_report_{report_str}.pdf"
    
    font_prop = fm.FontProperties(fname=FONT_PATH, size=12)

    if not os.path.exists(INPUT_PATH):
        print(f"[WARN] 입력 파일이 존재하지 않음: {INPUT_PATH}")
        return

    spark = SparkSession.builder.appName("DailyNewsReport").getOrCreate()

    # JSON 읽기
    df = spark.read.json(INPUT_PATH, multiLine=True)
    
    def parse_and_clean_keywords(keywords_str):
        import json
        try:
            keywords = json.loads(keywords_str)
            return [kw.strip().lower() for kw in keywords if kw.strip()]
        except:
            return []

    parse_keywords_udf = udf(parse_and_clean_keywords, ArrayType(StringType()))

    # 키워드 정제 및 추출
    df = df.withColumn("keywords_array", parse_keywords_udf(col("keywords")))
    df_filtered = df \
        .withColumn("keyword", explode("keywords_array")) \
        .select("write_date", "keyword")

    df_filtered.show(truncate=False)

    # 키워드 집계 (정제된 데이터 기준)
    top_keywords_df = df_filtered \
        .groupBy("keyword") \
        .count() \
        .sort("count", ascending=False) \
        .limit(10)

    # Pandas 변환 또는 collect()로 시각화
    keyword_data = top_keywords_df.collect()
    keywords = [row["keyword"] for row in keyword_data]
    counts = [row["count"] for row in keyword_data]

    # 시각화
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(keywords[::-1], counts[::-1])

    # 막대 위에 숫자 표시
    for bar, count in zip(bars, counts[::-1]):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.2, str(count),
                ha='center', va='bottom', fontproperties=font_prop)

    ax.set_title(f"{yester_title_str} 뉴스 키워드 TOP 10", fontproperties=font_prop)
    ax.set_xlabel("키워드", fontproperties=font_prop)
    ax.set_ylabel("빈도수", fontproperties=font_prop)
    plt.xticks(rotation=45, ha='right', fontproperties=font_prop)
    plt.tight_layout()

    # 생성된 daily_report_YYYYMMDD.pdf는 로컬 파일 시스템에 저장
    plt.savefig(REPORT_PATH)
    print(f"[INFO] 리포트 저장 완료: {REPORT_PATH}")

    os.makedirs(os.path.dirname(ARCHIVE_PATH), exist_ok=True)
    shutil.move(INPUT_PATH, ARCHIVE_PATH)
    print(f"[INFO] JSON 파일 이동 완료: {ARCHIVE_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spark를 이용한 일일 뉴스 리포트 생성")
    parser.add_argument("--date", required=True, help="보고서 기준 날짜 (YYYY-MM-DD)")
    args = parser.parse_args()

    main(args.date)
