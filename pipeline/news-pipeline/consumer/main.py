from config.settings import settings
from config.logging import log

from kafka_client.consumer import build_consumer, process_article


def main() -> None:
    log.info("Consumer start: topic=%s, bootstrap=%s, group=%s",
             settings.KAFKA_TOPIC, settings.KAFKA_BOOTSTRAP_SERVERS, settings.KAFKA_GROUP_ID)

    consumer = build_consumer()

    try:
        for message in consumer:
            log.info("Kafka recv partition=%s offset=%s", message.partition, message.offset)
            process_article(message.value)
    except KeyboardInterrupt:
        log.info("Consumer stopped by user")
    finally:
        try:
            consumer.close()
        except Exception:
            pass
        log.info("Consumer shutdown")

if __name__ == "__main__":
    main()
