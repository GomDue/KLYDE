from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors import FlinkKafkaConsumer
import json
from models import NewsArticle
from producer.preprocessing import transform_classify_category, transform_extract_keywords, transform_to_embedding
from db import insert_into_postgres
from datetime import datetime

def process_article(raw_json):
    try:
        data = json.loads(raw_json)
        article = NewsArticle(**data)

        published = datetime.strptime(article.published, "%a, %d %b %Y %H:%M:%S %Z")
        result = {
            'title': article.title,
            'author': 'unknown',
            'published': published.strftime("%Y-%m-%d %H:%M:%S"),
            'content': article.content,
            'category': transform_classify_category(article.content),
            'link': article.link,
            'keywords': json.dumps(transform_extract_keywords(article.content)),
            'embedding': transform_to_embedding(article.content)
        }

        insert_into_postgres(result)

    except Exception as e:
        print(f"[오류] {e}")


def main():
    env = StreamExecutionEnvironment.get_execution_environment()

    kafka_consumer = FlinkKafkaConsumer(
        topics='news_topic',
        deserialization_schema=SimpleStringSchema(),
        properties={
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'flink-test-group',
            'auto.offset.reset': 'earliest'
        }
    )

    stream = env.add_source(kafka_consumer)

    # Kafka 메시지 로깅
    stream.map(lambda x: f"[Kafka 수신] {x}").print()

    # 실제 기사 처리 및 DB 저장
    stream.map(process_article)

    env.execute("SimpleKafkaPrint")


if __name__ == '__main__':
    print("[DEBUG] 실행 시작")
    main()




# def main():
#     env = StreamExecutionEnvironment.get_execution_environment()

#     kafka_consumer = FlinkKafkaConsumer(
#         topics='news_topic',
#         deserialization_schema=SimpleStringSchema(),
#         properties={
#             'bootstrap.servers': 'localhost:9092',
#             'group.id': 'flink-test-group',
#             'auto.offset.reset': 'earliest'
#         }
#     )

#     stream = env.add_source(kafka_consumer)

#     stream.map(lambda x: f"[Kafka 수신] {x}").print()
#     # stream.map(process_article)

#     env.execute("SimpleKafkaPrint")


# print("[DEBUG] 실행 시작")  # 디버깅용 로그
# main()
