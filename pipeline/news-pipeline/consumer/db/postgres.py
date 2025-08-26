import json
from db.connection import get_postgres_conn


def insert_postgres(news_data):
    conn = get_postgres_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO news_article 
        (title, writer, write_date, content, category, url, keywords, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (url) DO NOTHING
    """, (
        news_data["title"],
        news_data["writer"],
        news_data["write_date"],
        news_data["content"],
        news_data["category"],
        news_data["url"],
        json.dumps(news_data["keywords"]),
        news_data["embedding"] if news_data["embedding"] else None
    ))
    
    conn.commit()
    cur.close()
    conn.close()
