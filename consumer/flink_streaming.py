from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors import FlinkKafkaConsumer
from models import NewsArticle
from preprocessing import transform_classify_category, transform_extract_keywords, transform_to_embedding
from db import insert_into_postgres
import json


def process_article(raw_json):
    try:
        data = json.loads(raw_json)
        article = NewsArticle(**data)

        result = {
            'title': article.title,
            'author': 'unknown',
            'content': article.content,
            'category': transform_classify_category(article),
            'keywords': transform_extract_keywords(article),
            'embedding': transform_to_embedding(article)
        }

        insert_into_postgres(result)

    except Exception as e:
        print(f"[오류] {e}")


def main():
    env = StreamExecutionEnvironment.get_execution_environment()

    kafka_consumer = FlinkKafkaConsumer(
        topics='news_topic',
        deserialization_schema=SimpleStringSchema(),
        properties={'bootstrap.servers': 'localhost:9092', 'group.id': 'flink-group'}
    )

    stream = env.add_source(kafka_consumer)

    stream.map(process_article)
    env.execute("NewsArticleProcessor")

if __name__ == '__main__':
    main()
