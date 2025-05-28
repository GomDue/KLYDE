import os
from datetime import datetime 
import json
import hashlib
import psycopg2
from dateutil import parser as date_parser
from models import NewsArticle
from preprocessing import *
from elasticsearch import Elasticsearch
from pyflink.common import Configuration
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors import FlinkKafkaConsumer
from hdfs import InsecureClient

FLINK_KAFKA_CONNECTOR_PATH = "file:///opt/streaming/config/flink-sql-connector-kafka-3.3.0-1.20.jar"
HDFS_HOST = "http://hadoop-namenode:9870"
ELASTICSEARCH_URL = ["http://elasticsearch1:9200", "http://elasticsearch2:9201", "http://elasticsearch3:9202"]
HDFS_DEST_PATH = "/data"


def hash_url(url):
    return hashlib.md5(url.encode()).hexdigest()


def insert_elasticsearch(data):
    es = Elasticsearch(
        ELASTICSEARCH_URL,
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    )
    index_name = "news"

    try:
        es_doc = {
            "title": data["title"],
            "content": data["content"],
            "writer": data["writer"],
            "category": data["category"],
            "keywords": data["keywords"],
            "write_date": data["write_date"]
        }
        es.update(
            index=index_name,
            id=data["url"],
            body={
                "doc": es_doc,
                "doc_as_upsert": True
            }
        )
        print(f"[ES 저장 완료] {data['title'][:50]}")
    except Exception as e:
        print(f"[ES 저장 실패] {e}")


def insert_postgres(data):
    try:
        conn = psycopg2.connect(
            host="postgres-news",
            dbname="news",
            user="ssafy",
            password="ssafy",
            port=5432
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO news_article 
            (title, writer, write_date, content, category, url, keywords, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING
        """, (
            data['title'],
            data['writer'],
            data['write_date'],
            data['content'],
            data['category'],
            data['url'],
            json.dumps(data['keywords']),
            f"[{','.join(map(str, data['embedding']))}]" 
        ))
        conn.commit()
        cur.close()
        conn.close()
        print(f"[DB 저장 성공] {data['title'][:50]}")
    except Exception as e:
        print(f"[DB 저장 실패] {e}")


def save_jsonl_to_hdfs(processed):
    hdfs_client = InsecureClient(HDFS_HOST, user="hadoop")
    
    url_hash = hash_url(processed["url"])  # URL을 해시화하여 파일 이름 생성
    file_name = f"{url_hash}.jsonl"  # 파일 이름으로 해시화된 URL 사용
    
    write_date = datetime.strptime(processed["write_date"], "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
    record = {
        "write_date": write_date,
        "keywords": processed["keywords"],
        "category": processed["category"],
        "url": processed["url"] 
    }
    
    partitioned_path = f"/data/{write_date}/"
    hdfs_file_path = os.path.join(partitioned_path, file_name)  # 전체 HDFS 경로

    json_line = json.dumps(record) + "\n"

    try:
        # 해당 경로가 없으면 새로 생성
        if not hdfs_client.status(partitioned_path, strict=False):
            hdfs_client.makedirs(partitioned_path)

        # 파일 존재 여부를 확인
        try:
            hdfs_client.status(hdfs_file_path)  # 파일 상태를 확인
            print(f"[Hadoop 저장 실패] {file_name} 이미 존재함, 중복된 URL은 건너뜁니다.")
        except:
            # 파일이 존재하지 않으면 새로 생성
            with hdfs_client.write(hdfs_file_path, encoding='utf-8') as writer:
                writer.write(json_line)
            print(f"[Hadoop 저장 완료] {file_name}에 데이터 저장됨")
    except Exception as e:
        print(f"[Hadoop 저장 실패] {e}")


def process_article(raw_json):
    try:
        data = json.loads(raw_json)
        article = NewsArticle(**data)

        print(f"[Kafka 수신] {data['title'][:50]}")

        content = preprocess_content(article.content)
        
        if article.link:
            processed = {
                'title': article.title,
                'writer': article.author or "unknown",
                'write_date': date_parser.parse(article.published).strftime("%Y-%m-%d %H:%M:%S"),
                'content': content,
                'category': transform_classify_category(content),
                'url': article.link,
                'keywords': transform_extract_keywords(content),
                'embedding': transform_to_embedding(content)
            }

            insert_postgres(processed)
            insert_elasticsearch(processed)
            save_jsonl_to_hdfs(processed)

    except Exception as e:
        print(f"[전처리 실패] {e}")


def main():
    config = Configuration()
    config.set_string("pipeline.jars", FLINK_KAFKA_CONNECTOR_PATH)

    env = StreamExecutionEnvironment.get_execution_environment(configuration=config)

    kafka_consumer = FlinkKafkaConsumer(
        topics='news_topic',
        deserialization_schema=SimpleStringSchema(),
        properties={
            'bootstrap.servers': 'host.docker.internal:9092',
            'group.id': 'flink-news-group',
            'auto.offset.reset': 'earliest'
        }
    )

    stream = env.add_source(kafka_consumer)

    stream.map(process_article)

    env.execute("News Kafka → PostgreSQL & HDFS Pipeline")


if __name__ == '__main__':
    main()
