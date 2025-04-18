import psycopg2

def insert_into_postgres(data):
    conn = psycopg2.connect(
        host="localhost",
        dbname="news",
        user="postgres",       
        password="1234",       
        port=5432
    )
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO news_article (title, writer, write_date, content, category, url, keywords, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['title'],
        data.get('author', 'unknown'),
        data['published'],
        data['content'],
        data['category'],
        data['link'],
        data['keywords'],
        data['embedding']
    ))
    conn.commit()
    cur.close()
    conn.close()
