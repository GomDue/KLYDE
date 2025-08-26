import json
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, explode
from pyspark.sql.types import ArrayType, StringType
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm



def load_all_data_from_hdfs(spark, date_str):
    input_dir = f"/data/{date_str}/"
    all_df = None

    try:        
        file_list = client.list(input_dir)
        print(f"[INFO] 파일 목록: {file_list}") 
        
        for file_name in file_list:
            if file_name.endswith('.json'):
                file_path = f"hdfs://hadoop-namenode:9000/data/{date_str}/{file_name}"
                try:
                    df = spark.read.json(file_path, multiLine=True)
                    all_df = df if all_df is None else all_df.union(df)
                except Exception as e:
                    print(f"[ERROR] Spark에서 파일 읽기 실패: {file_path}, 원인: {e}")
                    continue

        if all_df is None:
            print(f"[WARN] 유효한 JSON 파일이 없어 DataFrame을 생성하지 못했습니다.")
            return None

        return all_df

    except Exception as e:
        print(f"[WARN] HDFS 파일 읽기 실패: {input_dir}, 오류: {e}")
        return None

# 원본 기사 병합 저장 (중간 저장 X)
def merge_raw_articles_to_archive(yester_str):
    """
    /data/{날짜}/ 에 있는 모든 .json 파일을 병합하여
    /data/archive/{날짜}/merged.json 로 저장
    """
    input_dir = f"/data/{yester_str}/"
    output_dir = f"/data/archive/{yester_str}/"
    output_path = f"{output_dir}merged.json"

    try:
        if not client.status(output_dir, strict=False):
            client.makedirs(output_dir)

        file_list = client.list(input_dir)
        with client.write(output_path, encoding='utf-8', overwrite=True) as writer:
            for file in file_list:
                if file.endswith('.json'):
                    full_path = f"{input_dir}{file}"
                    with client.read(full_path, encoding='utf-8') as reader:
                        writer.write(reader.read())
        print(f"[HDFS] 병합 완료: {output_path}")
    except Exception as e:
        print(f"[ERROR] 병합 실패: {e}")

def parse_and_clean_keywords(keywords_str):
    try:
        if isinstance(keywords_str, str):
            keywords = json.loads(keywords_str)
        else:
            keywords = keywords_str
        return [kw.strip().lower() for kw in keywords if kw.strip()]
    except Exception as e:
        print(f"[WARN] keywords 파싱 실패: {e}")
        return []

def count_by_category(df):
    return df.groupBy("category").count().sort("count", ascending=False)

def count_by_keyword(df):
    df = df.withColumn("keywords_array", udf(parse_and_clean_keywords, ArrayType(StringType()))(col("keywords")))
    df = df.withColumn("keyword", explode(col("keywords_array")))
    return df.groupBy("keyword").count().sort("count", ascending=False).limit(10)

def plot_keyword_counts(keywords, counts, yester_title_str, font_prop):
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(keywords[::-1], counts[::-1], label='Keywords', color='skyblue', alpha=0.7)

    for bar, count in zip(bars, counts[::-1]):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.2, str(count),
                ha='center', va='bottom', fontproperties=font_prop)

    ax.set_title(f"{yester_title_str} News Keywords TOP 10", fontproperties=font_prop)
    ax.set_xlabel("Keywords", fontproperties=font_prop)
    ax.set_ylabel("Frequency", fontproperties=font_prop)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.axhline(y=0, color='black', linewidth=1)

def plot_category_counts(categories, category_counts, yester_title_str, font_prop):
    fig, ax = plt.subplots(figsize=(10, 6))
    category_bars = ax.barh(categories[::-1], category_counts[::-1], label='Categories', color='lightgreen', alpha=0.6)

    for bar, count in zip(category_bars, category_counts[::-1]):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2, str(count),
                ha='left', va='center', fontproperties=font_prop)

    ax.set_title(f"{yester_title_str} News Category TOP", fontproperties=font_prop)
    ax.set_xlabel("Frequency", fontproperties=font_prop)
    ax.set_ylabel("Category", fontproperties=font_prop)
    ax.tick_params(axis='y', rotation=0, labelsize=10)
    ax.tick_params(axis='x', labelsize=10)

def main():
    report_date = datetime.today()
    yester_date = report_date - timedelta(days=1)
    yester_str = yester_date.strftime("%Y%m%d")
    report_str = report_date.strftime("%Y%m%d")
    yester_title_str = yester_date.strftime("%Y-%m-%d")

    print(f"[INFO] 리포트 기준 날짜: {report_str}")

    FONT_PATH = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    REPORT_PATH = f"/opt/airflow/data/daily_report_{report_str}.pdf"
    font_prop = fm.FontProperties(fname=FONT_PATH, size=12)

    spark = SparkSession.builder \
        .appName("DailyNewsReport") \
        .master("spark://spark-master:7077") \
        .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop-namenode:9000") \
        .getOrCreate()

    df = load_all_data_from_hdfs(spark, yester_str)
    if df is None:
        print(f"[ERROR] HDFS에서 데이터를 읽을 수 없습니다.")
        return

    category_count_df = count_by_category(df)
    category_count_df.show()
    top_keywords_df = count_by_keyword(df)
    top_keywords_df.show()

    keyword_data = top_keywords_df.collect()
    keywords = [row["keyword"] for row in keyword_data]
    counts = [row["count"] for row in keyword_data]

    category_data = category_count_df.collect()
    categories = [row["category"] for row in category_data]
    category_counts = [row["count"] for row in category_data]

    # 그래프 생성 및 저장
    plot_keyword_counts(keywords, counts, yester_title_str, font_prop)
    plot_category_counts(categories, category_counts, yester_title_str, font_prop)
    plt.tight_layout()
    plt.savefig(REPORT_PATH)
    print(f"[INFO] 리포트 저장 완료: {REPORT_PATH}")

    # 원본 기사 병합하여 archive 저장
    merge_raw_articles_to_archive(yester_str)

if __name__ == "__main__":
    main()
