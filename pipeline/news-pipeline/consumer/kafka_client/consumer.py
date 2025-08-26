import json
from kafka import KafkaConsumer
from dateutil import parser as date_parser

from config.settings import settings
from config.logging import log
from models.news import NewsArticle
from processing.preprocess import preprocess_content
from db.postgres import insert_postgres
from db.elastic import insert_elasticsearch


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
    data = json.loads(raw_news)
    article = NewsArticle(**data)

    log.info("Received: %s", article.title)

    if article.link:
        processed = {
            "title":      article.title,
            "writer":     article.author or "Unknown",
            "write_date": date_parser.parse(article.published).strftime("%Y-%m-%d %H:%M:%S"),
            "content":    preprocess_content(article.content),
            "category":   "Unclassified", # transform_classify_category(content),
            "url":        article.link,
            "keywords":   [], # transform_extract_keywords(content),
            "embedding":  None, # transform_to_embedding(content)
        }

        try:
            insert_postgres(processed)
            log.info("DB OK: %s", article.title)
        except Exception:
            log.exception("DB insert failed: %s", article.title)
            return  # DB 실패 시 ES 색인은 건너뜀

        try:
            insert_elasticsearch(processed)
            log.info("ES OK: %s", article.title)
        except Exception:
            log.exception("ES index failed: %s", article.title)
