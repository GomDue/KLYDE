import psycopg2

def insert_into_postgres(data):
    conn = psycopg2.connect(
        host="localhost",
        dbname="news_db",
        user="postgres",       
        password="1234",       
        port=5432
    )
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO news_articles (title, author, content, category, keywords, embedding_json)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data['title'],
        data.get('author', 'unknown'),
        data['content'],
        data['category'],
        data['keywords'],
        data['embedding']
    ))
    conn.commit()
    cur.close()
    conn.close()
