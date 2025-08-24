import psycopg2
from elasticsearch import Elasticsearch
from config.settings import settings

def get_conn():
    return psycopg2.connect(
        host=settings.POSTGRESQL_HOST,
        dbname=settings.POSTGRESQL_DB,
        user=settings.POSTGRESQL_USER,
        password=settings.POSTGRESQL_PASSWORD,
        port=settings.POSTGRESQL_PORT,
    )

def get_elastic_conn():
    return Elasticsearch(
        settings.ES_HOSTS,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )

