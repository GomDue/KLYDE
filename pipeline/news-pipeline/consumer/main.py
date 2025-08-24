from config.settings import settings
from config.logging import setup_logging
from kafka_client.consumer import build_consumer, process_article


def main() -> None:
    setup_logging(settings.LOG_LEVEL)
    consumer = build_consumer()

    print("[Kafka Consumer 시작]")

    for message in consumer:
        process_article(message.value)


if __name__ == '__main__':
    main()