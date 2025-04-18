import feedparser
import psycopg2
from dateutil import parser as dateparser

# ZDNet Korea RSS 주소
rss_url = "https://www.zdnet.com/news/rss.xml"

# PostgreSQL 연결
conn = psycopg2.connect(
    host="localhost",
    dbname="news",
    user="postgres",       # 또는 news_user
    password="1234",       # 설정한 비밀번호
    port=5432
)
cursor = conn.cursor()

# RSS 파싱
feed = feedparser.parse(rss_url)

for entry in feed.entries:
    title = entry.get('title')
    link = entry.get('link')
    description = entry.get('description', '')

    # pubDate는 날짜 문자열이므로 dateparser로 변환
    pubDate_str = entry.get('published', '') or entry.get('pubDate', '')
    pubDate = None
    try:
        pubDate = dateparser.parse(pubDate_str).date() if pubDate_str else None
    except Exception as e:
        print(f"[날짜 변환 실패] {title}: {e}")

    # author 필드는 없는 경우가 많음
    author = entry.get('author', None)

    try:
        cursor.execute("""
            INSERT INTO news_zdnet_raw (title, link, description, pubDate, author)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (link) DO NOTHING;
        """, (title, link, description, pubDate, author))
    except Exception as e:
        print(f"[저장 실패] {title}: {e}")

conn.commit()
cursor.close()
conn.close()

print("ZDNet Korea 뉴스 저장 완료!")
