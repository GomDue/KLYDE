import feedparser
import requests
from bs4 import BeautifulSoup
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
)

seen_links = set()
RSS_FEED_URL = 'http://feeds.bbci.co.uk/news/rss.xml'
TOPIC_NAME = 'news_topic'

def fetch_and_send_articles():
    feed = feedparser.parse(RSS_FEED_URL)
    for entry in feed.entries:
        link = entry.link
        if link in seen_links:
            continue
        seen_links.add(link)

        try:
            res = requests.get(link)
            soup = BeautifulSoup(res.text, 'html.parser')
            paragraphs = soup.select('article div[data-component="text-block"] p')
            article_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
            if not article_text:
                article_text = '본문 없음'

            article_data = {
                'title': entry.title,
                'link': link,
                'published': entry.published,
                'content': article_text
            }

            producer.send(TOPIC_NAME, value=article_data)
            print(f"[전송 완료] {entry.title}")
        except Exception as e:
            print(f"[오류] {link} - {e}")

if __name__ == '__main__':
    while True:
        fetch_and_send_articles()
        time.sleep(300)
