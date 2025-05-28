import os
from datetime import datetime 
import json
import psycopg2
from dateutil import parser as date_parser
from models import NewsArticle
from preprocessing import (
    transform_classify_category,
    transform_extract_keywords,
    transform_to_embedding,
    preprocess_content
)

from pyflink.common import Configuration
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors import FlinkKafkaConsumer
from hdfs import InsecureClient

FLINK_KAFKA_CONNECTOR_PATH = "file:///opt/streaming/config/flink-sql-connector-kafka-3.3.0-1.20.jar"
HDFS_HOST = "http://hadoop-namenode:9870"


def insert_article(data):
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
    DEST_PATH = "/data"
    file_name = datetime.strptime(processed['write_date'], "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d") + ".jsonl"
    hdfs_file_path = os.path.join(DEST_PATH, file_name)

    record = {
        "write_date": processed["write_date"],
        "keywords": processed["keywords"],
        "category": processed["category"]
    }

    json_line = json.dumps(record) + "\n"

    try:
        file_list = hdfs_client.list(DEST_PATH)
        lines = []  

        if file_name in file_list:
            with hdfs_client.read(hdfs_file_path, encoding='utf-8') as reader:
                lines = reader.readlines()

        lines.append(json_line)

        with hdfs_client.write(hdfs_file_path, overwrite=True, encoding='utf-8') as writer:
            writer.write(''.join(lines))
        print(f"[Hadoop 저장 완료] {file_name}에 키워드 저장됨")
    except Exception as e:
        print(f"[Hadoop 저장 실패] {e}")


def process_article(raw_json):
    try:
        data = json.loads(raw_json)
        article = NewsArticle(**data)

        print(f"[Kafka 수신] {data['title'][:50]}")

        content = preprocess_content(article.content)

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

        insert_article(processed)
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
