# nyt_rss_parsing.py
import feedparser
import psycopg2
from dateutil import parser as dateparser

rss_url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"

conn = psycopg2.connect(
    host="localhost",
    dbname="news_db",
    user="postgres",
    password="1234",
    port=5432
)
cursor = conn.cursor()
feed = feedparser.parse(rss_url)

for entry in feed.entries:
    title = entry.get('title')
    link = entry.get('link')
    description = entry.get('summary', '')
    pubDate_str = entry.get('published', '') or entry.get('pubDate', '')
    pubDate = dateparser.parse(pubDate_str).date() if pubDate_str else None
    creator = entry.get('author', '')  # NYT는 author로 들어오는 경우 있음

    try:
        cursor.execute("""
            INSERT INTO news_nyt_raw (title, link, description, pubDate, creator)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (link) DO NOTHING;
        """, (title, link, description, pubDate, creator))
    except Exception as e:
        print(f"[NYT 저장 실패] {title}: {e}")

conn.commit()
cursor.close()
conn.close()
print("NYT 뉴스 저장 완료!")
