import json
import logging
import feedparser
from kafka import KafkaProducer
from config.settings import settings
from utils.hashing import hash_url
from rss.sources import NEWS_SOURCES

logger = logging.getLogger("producer")


def build_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        client_id=settings.KAFKA_CLIENT_ID,
        acks=settings.KAFKA_ACKS,
        linger_ms=settings.KAFKA_LINGER_MS,
        batch_size=settings.KAFKA_BATCH_SIZE,
        compression_type=settings.KAFKA_COMPRESSION,
        key_serializer=lambda k: k.encode("utf-8"),
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'),
    )


def fetch_and_send() -> int:
    producer = build_producer()
    sent = 0

    for source in NEWS_SOURCES:
        name, rss_url, scraper = source["name"], source["rss_url"], source["scraper"]

        logger.info(f"RSS 파싱: {name}")
        feed = feedparser.parse(rss_url)

        for entry in feed.entries:
            try:
                link = entry.get("link")
                if not link:
                    continue

                key = hash_url(link)
                msg = {
                    "title": entry.get("title"),
                    "link": link,
                    "description": entry.get("summary", "") or entry.get("description", ""),
                    "published": entry.get("published", "") or entry.get("pubDate", ""),
                    "author": entry.get("author", None),
                    "content": scraper(link),
                    "source": name,
                }

                producer.send(settings.KAFKA_TOPIC, key=key, value=msg)
                sent += 1

            except Exception as e:
                logger.warning(f"[{source.name}] 항목 처리 실패: {e}")
                
    producer.flush()

    logger.info(f"전송 완료: {sent}건")
    return sent
