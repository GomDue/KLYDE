from pydantic import BaseSettings, Field
from typing import List

class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"

    # Kafka
    KAFKA_TOPIC: str = "news_topic"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    KAFKA_GROUP_ID: str = "news-consumer"

    # Postgres
    POSTGRESQL_HOST: str
    POSTGRESQL_DB: str
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_PORT: int

    # Elasticsearch
    ES_HOSTS: List[str] = Field(
        default_factory=lambda: [
            "http://elasticsearch1:9200",
            "http://elasticsearch2:9200",
        ]
    )

    class Config:
        env_file = "consumer.env"
        case_sensitive = False


settings = Settings()
