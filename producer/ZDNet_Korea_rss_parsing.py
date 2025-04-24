import feedparser
import psycopg2
from dateutil import parser as dateparser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def get_zdnet_article_content(link: str) -> str:
    options = Options()
    options.add_argument("--headless")  # 브라우저 없이 실행
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(link)
        time.sleep(3)  # JS 렌더링 기다리기
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 본문 선택
        paragraphs = soup.select('div.c-articleContent p')
        article_texts = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text and not text.lower().startswith('also') and 'zdnet' not in text.lower():
                article_texts.append(text)

        article_text = ' '.join(article_texts)
        return article_text if article_text else '본문 없음'

    except Exception as e:
        print(f"[본문 크롤링 실패] {link}: {e}")
        return '본문 파싱 실패'
    finally:
        driver.quit()

# RSS Feed URL
rss_url = "https://www.zdnet.com/news/rss.xml"

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
    description = entry.get('description', '')

    # pubDate 처리
    pubDate_str = entry.get('published', '') or entry.get('pubDate', '')
    pubDate = None
    try:
        pubDate = dateparser.parse(pubDate_str) if pubDate_str else None
    except Exception as e:
        print(f"[날짜 변환 실패] {title}: {e}")

    author = entry.get('author', None)

    # 본문 크롤링
    content = get_zdnet_article_content(link)

    try:
        cursor.execute("""
            INSERT INTO news_zdnet_raw (title, link, description, pubDate, author, content)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (link) DO NOTHING;
        """, (title, link, description, pubDate, author, content))
    except Exception as e:
        print(f"[ZDNet Korea 저장 실패] {title}: {e}")

# 종료
conn.commit()
cursor.close()
conn.close()

print("ZDNet Korea 뉴스 저장 완료")
