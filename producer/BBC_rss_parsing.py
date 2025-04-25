import feedparser
import psycopg2
from dateutil import parser as dateparser
import requests
from bs4 import BeautifulSoup

def get_bbc_article_content(link: str) -> str:
    try:
        res = requests.get(link, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        paragraphs = soup.select('article div[data-component="text-block"] p')
        article_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
        return article_text if article_text else None
    except Exception as e:
        print(f"[본문 크롤링 실패] {link}: {e}")
        return '본문 파싱 실패'

# RSS Feed URL
rss_url = "http://feeds.bbci.co.uk/news/rss.xml"

# PostgreSQL 연결
conn = psycopg2.connect(
    host="localhost",
    dbname="news",
    user="postgres",
    password="1234",
    port=5432
)
cursor = conn.cursor()

# RSS 파싱
feed = feedparser.parse(rss_url)

for entry in feed.entries:
    title = entry.get('title')
    link = entry.get('link')
    description = entry.get('summary', '')
    pubDate_str = entry.get('published', '') or entry.get('pubDate', '')
    pubDate = dateparser.parse(pubDate_str).date() if pubDate_str else None

    content = get_bbc_article_content(link)
    if content:
        try:
            cursor.execute("""
                INSERT INTO news_bbc_raw (title, link, description, pubDate, content)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (link) DO NOTHING;
            """, (title, link, description, pubDate, content))
        except Exception as e:
            print(f"[BBC 저장 실패] {title}: {e}")

# 종료
conn.commit()
cursor.close()
conn.close()
print("BBC 뉴스 저장 완료!")
