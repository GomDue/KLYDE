import feedparser
import psycopg2
from dateutil import parser as dateparser
import requests
from bs4 import BeautifulSoup

def get_nippon_article_content(link: str) -> str:
    try:
        res = requests.get(link, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')

        # editArea 안의 <p> 중 class 없는 문단만 추출
        paragraphs = soup.select('div.editArea > p')
        pure_texts = [
            p.get_text(strip=True)
            for p in paragraphs
            if not p.has_attr('class') and p.get_text(strip=True)
        ]

        article_text = ' '.join(pure_texts)
        return article_text if article_text else '본문 없음'

    except Exception as e:
        print(f"[본문 크롤링 실패] {link}: {e}")
        return '본문 파싱 실패'

# RSS Feed URL
rss_url = "https://www.nippon.com/en/feed/"

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
    description = entry.get('summary', '') or entry.get('description', '')
    pubDate_str = entry.get('published', '') or entry.get('pubDate', '')
    pubDate = dateparser.parse(pubDate_str) if pubDate_str else None

    content = get_nippon_article_content(link)

    try:
        cursor.execute("""
            INSERT INTO news_nippon_raw (title, link, description, pubDate, content)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (link) DO NOTHING;
        """, (title, link, description, pubDate, content))
    except Exception as e:
        print(f"[Nippon 저장 실패] {title}: {e}")

# 종료
conn.commit()
cursor.close()
conn.close()
print("Nippon 뉴스 저장 완료!")
