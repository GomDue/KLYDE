import json
import logging
from kafka import KafkaConsumer
from dateutil import parser as date_parser
from config.settings import settings
from models.news import NewsArticle
from processing.preprocess import preprocess_content
from db.postgres import insert_postgres
from db.elastic import insert_elasticsearch

logger = logging.getLogger("consumer")


def build_consumer() -> KafkaConsumer:
    return KafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_GROUP_ID,
        enable_auto_commit=True, 
        auto_offset_reset="earliest",
        value_deserializer=lambda x: x.decode("utf-8"),
    )


def process_article(raw_news) -> None:
    try:
        data = json.loads(raw_news)
        article = NewsArticle(**data)

        print(f"[Kafka 수신] {data['title'][:50]}")

        if article.link:
            processed = {
                'title': article.title,
                'writer': article.author or "unknown",
                'write_date': date_parser.parse(article.published).strftime("%Y-%m-%d %H:%M:%S"),
                'content': preprocess_content(article.content),
                'category': "미분류", # transform_classify_category(content),
                'url': article.link,
                'keywords': [], # transform_extract_keywords(content),
                'embedding': None, # transform_to_embedding(content)
            }

            insert_postgres(processed)
            insert_elasticsearch(processed)

    except Exception as e:
        print(f"[전처리 실패] {e}")
