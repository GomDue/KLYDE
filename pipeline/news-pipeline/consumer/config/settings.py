from pydantic import BaseSettings, Field
from typing import List


class Settings(BaseSettings):
    # Log
    LOG_LEVEL: str = "INFO"
    LOG_PATH: str = "/opt/news-pipeline/logs/consumer.log"

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

    # GPT
    OPENAI_API_KEY: str
    GPT_MODEL:str = "gpt-4o-mini"
    EMBEDDING_MODEL:str = "text-embedding-3-small"
    NEWS_CATEGORIES = [
        "SciTech", "Health", "Economy", "Education", "International", "Lifestyle",
        "Culture", "Accidents", "Society", "Industry", "Sports", "Femcare",
        "TripLeisure", "Entertainment", "Politics", "Local", "Hobbies",
    ]
    NEWS_CATEGORIES_STR: str = ", ".join(NEWS_CATEGORIES)


    class Config:
        env_file = "consumer.env"
        case_sensitive = False


settings = Settings()
