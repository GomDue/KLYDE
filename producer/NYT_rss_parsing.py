import feedparser
import psycopg2
from dateutil import parser as dateparser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def get_nyt_article_content(link: str) -> str:
    options = Options()
    options.add_argument("--headless")  # 브라우저 창 없이 실행
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)  # chromedriver 경로를 PATH에 포함시켰다면 생략 가능

    try:
        driver.get(link)
        time.sleep(3)  # JS 로딩 대기
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 본문 파싱
        paragraphs = soup.select('section[name="articleBody"] p')
        article_text = ' '.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        return article_text if article_text else '본문 없음'

    except Exception as e:
        print(f"[본문 크롤링 실패] {link}: {e}")
        return '본문 파싱 실패'

    finally:
        driver.quit()

# RSS Feed URL
rss_url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"

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
    pubDate = dateparser.parse(pubDate_str) if pubDate_str else None
    creator = entry.get('author', '')

    content = get_nyt_article_content(link)

    try:
        cursor.execute("""
            INSERT INTO news_nyt_raw (title, link, description, pubDate, creator, content)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (link) DO NOTHING;
        """, (title, link, description, pubDate, creator, content))
    except Exception as e:
        print(f"[NYT 저장 실패] {title}: {e}")

# 종료
conn.commit()
cursor.close()
conn.close()
print("NYT 뉴스 저장 완료!")
