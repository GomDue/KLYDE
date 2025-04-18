# nippon_rss_parsing.py
import feedparser
import psycopg2
from dateutil import parser as dateparser

rss_url = "https://www.nippon.com/en/feed/"

conn = psycopg2.connect(
    host="localhost",
    dbname="news",
    user="postgres",
    password="1234",
    port=5432
)
cursor = conn.cursor()
feed = feedparser.parse(rss_url)

for entry in feed.entries:
    title = entry.get('title')
    link = entry.get('link')
    description = entry.get('summary', '') or entry.get('description', '')
    pubDate_str = entry.get('published', '') or entry.get('pubDate', '')
    pubDate = dateparser.parse(pubDate_str).date() if pubDate_str else None

    try:
        cursor.execute("""
            INSERT INTO news_nippon_raw (title, link, description, pubDate)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (link) DO NOTHING;
        """, (title, link, description, pubDate))
    except Exception as e:
        print(f"[Nippon 저장 실패] {title}: {e}")

conn.commit()
cursor.close()
conn.close()
print("Nippon 뉴스 저장 완료!")
