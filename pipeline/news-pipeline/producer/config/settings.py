from pydantic import BaseSettings


class Settings(BaseSettings):
    # Log
    LOG_LEVEL: str = "INFO"
    LOG_PATH: str = "/logs/producer.log"

    # Kafka
    KAFKA_TOPIC: str = "news_topic"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"

    # Kafka Producer
    KAFKA_CLIENT_ID: str = "rss-producer"
    KAFKA_ACKS: str = "all"
    KAFKA_LINGER_MS: int
    KAFKA_BATCH_SIZE: int
    KAFKA_COMPRESSION: str = "gzip" # gzip|lz4|snappy|zstd


    class Config:
        env_file = "producer.env"
        case_sensitive = False


settings = Settings()
