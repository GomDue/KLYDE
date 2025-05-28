# import os
# from datetime import datetime, timedelta

# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, explode, udf
# from pyspark.sql.types import ArrayType, StringType
# import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm
# from hdfs import InsecureClient

# def main():
#     # 날짜 처리
#     report_date = datetime.today()
#     yester_date = report_date - timedelta(days=1)

#     yester_str = yester_date.strftime("%Y%m%d")
#     report_str = report_date.strftime("%Y%m%d")
#     yester_title_str = yester_date.strftime("%Y-%m-%d")

#     print(f"[INFO] 리포트 기준 날짜: {report_str}")
    
#     # 경로 설정
#     FONT_PATH = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
#     INPUT_PATH = f"hdfs://hadoop-namenode:9000/data/{yester_str}.jsonl"
#     REPORT_PATH = f"/opt/airflow/data/daily_report_{report_str}.pdf"
#     ARCHIVE_PATH = f"/opt/airflow/data/news_archive/{yester_str}.jsonl"

#     font_prop = fm.FontProperties(fname=FONT_PATH, size=12)

#     # Spark 세션 시작
#     spark = SparkSession.builder \
#         .appName("DailyNewsReport") \
#         .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop-namenode:9000") \
#         .getOrCreate()

#     # 입력 경로에서 JSONL 읽기
#     try:
#         df = spark.read.json(INPUT_PATH, multiLine=False)  # multiLine=False
#         df.show(truncate=False)
#     except Exception as e:
#         print(f"[WARN] HDFS 파일 읽기 실패: {INPUT_PATH}, 오류: {e}")
#         return

#     def parse_and_clean_keywords(keywords_str):
#         import json
#         try:
#             if isinstance(keywords_str, str):
#                 keywords = json.loads(keywords_str)
#             else:
#                 keywords = keywords_str
#             return [kw.strip().lower() for kw in keywords if kw.strip()]
#         except Exception as e:
#             print(f"[WARN] keywords 파싱 실패: {e}")
#             return []

#     parse_keywords_udf = udf(parse_and_clean_keywords, ArrayType(StringType()))

#     # 'keywords' 컬럼이 문자열일 경우, 이를 정리하여 'keywords_array' 컬럼을 생성
#     df = df.withColumn("keywords_array", parse_keywords_udf(col("keywords")))

#     # explode 'keywords'와 'category' 컬럼을 함께 처리하여 워드 카운트
#     df_filtered = df.withColumn("keyword", explode("keywords_array")) \
#                     .select("write_date", "category", "keyword")

#     # keywords와 category 데이터 확인
#     df_filtered.show(truncate=False)

#     # 카테고리별로 카운트
#     category_count_df = df_filtered \
#         .groupBy("category") \
#         .count() \
#         .sort("count", ascending=False)

#     # category top 카운트 확인
#     category_count_df.show(truncate=False)

#     # keyword 카운트
#     top_keywords_df = df_filtered \
#         .groupBy("keyword") \
#         .count() \
#         .sort("count", ascending=False) \
#         .limit(10)

#     # keywords top 10 확인
#     top_keywords_df.show(truncate=False)

#     keyword_data = top_keywords_df.collect()
#     keywords = [row["keyword"] for row in keyword_data]
#     counts = [row["count"] for row in keyword_data]

#     # 카테고리 카운트 데이터
#     category_data = category_count_df.collect()
#     categories = [row["category"] for row in category_data]
#     category_counts = [row["count"] for row in category_data]

#     # 하나의 figure에서 두 개의 axes로 그래프를 그리기
#     fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

#     # 키워드 시각화
#     bars = ax1.bar(keywords[::-1], counts[::-1], label='Keywords', color='skyblue', alpha=0.7)

#     for bar, count in zip(bars, counts[::-1]):
#         height = bar.get_height()
#         ax1.text(bar.get_x() + bar.get_width() / 2, height + 0.2, str(count),
#                 ha='center', va='bottom', fontproperties=font_prop)

#     ax1.set_title(f"{yester_title_str} News Keywords TOP 10", fontproperties=font_prop)
#     ax1.set_xlabel("Keywords", fontproperties=font_prop)
#     ax1.set_ylabel("Frequency", fontproperties=font_prop)
#     ax1.tick_params(axis='x', rotation=45, labelsize=10)
#     ax1.tick_params(axis='y', labelsize=10)

#     # 그래프 사이에 구분선 추가
#     ax1.axhline(y=0, color='black', linewidth=1)

#     # 카테고리 시각화
#     category_bars = ax2.barh(categories[::-1], category_counts[::-1], label='Categories', color='lightgreen', alpha=0.6)

#     for bar, count in zip(category_bars, category_counts[::-1]):
#         ax2.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2, str(count),
#                 ha='left', va='center', fontproperties=font_prop)

#     ax2.set_title(f"{yester_title_str} News Category TOP", fontproperties=font_prop)
#     ax2.set_xlabel("Frequency", fontproperties=font_prop)
#     ax2.set_ylabel("Category", fontproperties=font_prop)
#     ax2.tick_params(axis='y', rotation=0, labelsize=10) 
#     ax2.tick_params(axis='x', labelsize=10)

#     plt.tight_layout()

#     # 파일로 저장
#     plt.savefig(REPORT_PATH)
#     print(f"[INFO] 리포트 저장 완료: {REPORT_PATH}")


#     # WebHDFS에서 로컬로 복사
#     client = InsecureClient("http://hadoop-namenode:9870", user="hadoop")
#     hdfs_path = f"/data/{yester_str}.jsonl"

#     try:
#         os.makedirs(os.path.dirname(ARCHIVE_PATH), exist_ok=True)
#         with client.read(hdfs_path, encoding='utf-8') as reader, open(ARCHIVE_PATH, 'w', encoding='utf-8') as writer:
#             for line in reader:
#                 writer.write(line)
#         print(f"[INFO] HDFS → 로컬 파일 복사 완료: {ARCHIVE_PATH}")
#     except Exception as e:
#         print(f"[WARN] HDFS 파일 복사 실패: {e}")

# if __name__ == "__main__":
#     main()


import json
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, explode
from pyspark.sql.types import ArrayType, StringType
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from hdfs import InsecureClient

# HDFS 클라이언트 연결
client = InsecureClient("http://hadoop-namenode:9870", user="hadoop")


def load_all_data_from_hdfs(spark, date_str):
    input_dir = f"/data/{date_str}/"
    
    try:        
        file_list = client.list(input_dir)
        print(f"[INFO] 파일 목록: {file_list}") 
        
        all_df = None
        for file_name in file_list:
            if file_name.endswith('.jsonl'):
                file_path = f"hdfs://hadoop-namenode:9000/data/{date_str}/{file_name}"
                df = spark.read.json(file_path, multiLine=False)
                if all_df is None:
                    all_df = df
                else:
                    all_df = all_df.union(df) 

        return all_df

    except Exception as e:
        print(f"[WARN] HDFS 파일 읽기 실패: {input_dir}, 오류: {e}")
        return None



# 중간 파일에 실시간 데이터 저장
def save_to_archive_file(data, yester_str):
    """
    실시간으로 데이터를 날짜별 중간 파일에 저장합니다.
    중간 파일에 append 방식으로 데이터를 추가합니다.
    """
    partitioned_path = f"/data/archive/{yester_str}/"
    archive_file_path = f"{partitioned_path}{yester_str}.jsonl"
    
    # JSON 형식으로 데이터 저장
    json_line = json.dumps(data) + "\n"
    try:
        # 해당 경로가 없으면 새로 생성
        if not client.status(partitioned_path, strict=False):
            client.makedirs(partitioned_path)

        # 중간 파일에 데이터를 추가
        with client.write(archive_file_path, append=True, encoding='utf-8') as writer:
            writer.write(json_line)
        print(f"[Hadoop] {yester_str}.jsonl에 데이터 추가됨")
    except Exception as e:
        print(f"[Hadoop 저장 실패] {e}")

# 중간 파일 병합 후 최종 파일로 저장
def merge_and_save_final_file(yester_str):
    """
    주기적으로 중간 파일을 병합하고, 불필요한 중간 파일을 삭제합니다.
    """
    final_file_path = f"/data/{yester_str}/{yester_str}.jsonl"
    archive_files = client.list(f"/data/archive/{yester_str}/")

    with client.write(final_file_path, encoding='utf-8', overwrite=True) as writer:
        for file in archive_files:
            if file.endswith('.jsonl'):
                with client.read(f"/data/archive/{yester_str}/{file}", encoding='utf-8') as reader:
                    writer.write(reader.read()) 

    # 병합 후 중간 파일 삭제
    for file in archive_files:
        if file.endswith('.jsonl'):
            client.delete(f"/data/archive/{yester_str}/{file}")
    print(f"[Hadoop] 최종 파일 {final_file_path}에 데이터 병합 완료, 중간 파일 삭제")

# 전처리 함수: keywords 파싱
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

# 데이터를 다루는 함수: 카운트 및 정렬
def count_by_category(df):
    category_count_df = df.groupBy("category") \
        .count() \
        .sort("count", ascending=False)
    return category_count_df

def count_by_keyword(df):
    df = df.withColumn("keywords_array", udf(parse_and_clean_keywords, ArrayType(StringType()))(col("keywords")))
    df = df.withColumn("keyword", explode(col("keywords_array")))

    top_keywords_df = df.groupBy("keyword") \
        .count() \
        .sort("count", ascending=False) \
        .limit(10)
    
    return top_keywords_df


# 그래프 그리기
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

    # 그래프 사이에 구분선 추가
    ax.axhline(y=0, color='black', linewidth=1)

    return fig

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

    return fig


def main():
    # 날짜 처리
    report_date = datetime.today()
    yester_date = report_date - timedelta(days=1)
    yester_str = yester_date.strftime("%Y%m%d")
    report_str = report_date.strftime("%Y%m%d")
    yester_title_str = yester_date.strftime("%Y-%m-%d")

    print(f"[INFO] 리포트 기준 날짜: {report_str}")

    # 경로 설정
    FONT_PATH = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    REPORT_PATH = f"/opt/airflow/data/daily_report_{report_str}.pdf"
    
    font_prop = fm.FontProperties(fname=FONT_PATH, size=12)

    # Spark 세션 시작
    spark = SparkSession.builder \
        .appName("DailyNewsReport") \
        .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop-namenode:9000") \
        .getOrCreate()

    df = load_all_data_from_hdfs(spark, yester_str)
    if df is None:
        print(f"[ERROR] HDFS에서 데이터를 읽을 수 없습니다.")
        return
    df.show()

    # 카테고리별, 키워드별 카운트
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

    # 그래프 생성
    plot_keyword_counts(keywords, counts, yester_title_str, font_prop)
    plot_category_counts(categories, category_counts, yester_title_str, font_prop)

    # 리포트 저장
    plt.tight_layout()
    plt.savefig(REPORT_PATH)
    print(f"[INFO] 리포트 저장 완료: {REPORT_PATH}")

    # 중간 파일 저장
    save_to_archive_file(data={"write_date": yester_str, "keywords": keywords, "category": categories}, yester_str=yester_str)

    # 배치 처리로 중간 파일 병합 및 삭제
    merge_and_save_final_file(yester_str=yester_str)

if __name__ == "__main__":
    main()
