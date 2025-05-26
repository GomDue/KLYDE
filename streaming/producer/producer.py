import feedparser
import json
import requests
import time
from bs4 import BeautifulSoup
from kafka import KafkaProducer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_content_bbc(link):
    try:
        res = requests.get(link, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        paras = soup.select('article div[data-component="text-block"] p')
        return ' '.join(p.get_text(strip=True) for p in paras)
    except Exception as e:
        print(f"[BBC 본문 실패] {e}")
        return ""

def get_content_nippon(link):
    try:
        res = requests.get(link, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        paras = soup.select('div.editArea > p')
        texts = [p.get_text(strip=True) for p in paras if not p.has_attr('class')]
        return ' '.join(texts)
    except Exception as e:
        print(f"[Nippon 본문 실패] {e}")
        return ""

def get_content_nyt(link):
    try:
        driver = get_driver()
        driver.get(link)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        paras = soup.select('section[name="articleBody"] p')
        return ' '.join(p.get_text(strip=True) for p in paras)
    except Exception as e:
        print(f"[NYT 본문 실패] {e}")
        return ""
    finally:
        driver.quit()

def get_content_zdnet(link):
    try:
        driver = get_driver()
        driver.get(link)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        paras = soup.select('div.c-articleContent p')
        return ' '.join(
            p.get_text(strip=True)
            for p in paras
            if 'zdnet' not in p.get_text(strip=True).lower()
        )
    except Exception as e:
        print(f"[ZDNet 본문 실패] {e}")
        return ""
    finally:
        driver.quit()

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)

# 각 뉴스사에 대한 설정
NEWS_SOURCES = [
    {
        "name": "BBC",
        "rss_url": "http://feeds.bbci.co.uk/news/rss.xml",
        "content_func": get_content_bbc
    },
    {
        "name": "Nippon",
        "rss_url": "https://www.nippon.com/en/feed/",
        "content_func": get_content_nippon
    },
    {
        "name": "NYT",
        "rss_url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "content_func": get_content_nyt
    },
    {
        "name": "ZDNet",
        "rss_url": "https://www.zdnet.com/news/rss.xml",
        "content_func": get_content_zdnet
    }
]

def send_news_to_kafka():
    producer = KafkaProducer(
        bootstrap_servers='host.docker.internal:9092',
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
    )

    for source in NEWS_SOURCES:
        print(f"▶ {source['name']} RSS 파싱 중...")
        feed = feedparser.parse(source['rss_url'])

        for entry in feed.entries:
            try:
                data = {
                    "title": entry.get("title"),
                    "link": entry.get("link"),
                    "description": entry.get("summary", "") or entry.get("description", ""),
                    "published": entry.get("published", "") or entry.get("pubDate", ""),
                    "author": entry.get("author", None),
                    "content": source["content_func"](entry.get("link")),
                    "source": source["name"]
                }
                producer.send("news_topic", value=data)
                print(f"  ✓ {source['name']} 기사 전송: {data['title'][:30]}...")
            except Exception as e:
                print(f"[{source['name']} 처리 실패] {e}")

    producer.flush()
    print("✅ 모든 뉴스사 데이터 Kafka 전송 완료")

if __name__ == "__main__":
    print("시작합니다!")
    while True:
        try:
            send_news_to_kafka()
        except Exception as e:
            print(f"[오류 발생] {e}")
        time.sleep(5)