def insert_into_postgres(conn, data):
    cur.execute("""
        INSERT INTO news_article (title, writer, write_date, content, category, url, keywords, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (url) DO NOTHING
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

