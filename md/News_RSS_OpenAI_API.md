# 📚 뉴스 데이터 수집 및 OpenAI 기반 키워드/임베딩 저장 프로젝트

## 1. 프로젝트 개요

본 프로젝트는 BBC, NYT, Nippon.com, ZDNet Korea 등 다양한 뉴스 플랫폼의 RSS 피드를 수집하여,  
PostgreSQL 데이터베이스에 저장한 후, OpenAI API를 활용하여  
- 뉴스 키워드 추출
- 뉴스 본문 임베딩(벡터화)  
작업을 수행하고 최종 결과를 데이터베이스에 저장하는 **엔드 투 엔드 데이터 파이프라인**을 구축하는 것을 목표로 한다.

---

## 2. 데이터 수집

- **수집 방식**: RSS Feed 기반 실시간 파싱
- **수집 대상**:
  - BBC: http://feeds.bbci.co.uk/news/rss.xml
  - NYT: https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml
  - Nippon.com: https://www.nippon.com/en/feed/
  - ZDNet Korea: https://www.zdnet.co.kr/news/news.xml
- **사용 라이브러리**:
  - `feedparser`
  - `psycopg2`
  - `python-dateutil`

- **저장 테이블 (Raw 데이터)**:
  - `news_bbc_raw`
  - `news_nyt_raw`
  - `news_zdnet_raw`
  - `news_nippon_raw`

---

## 3. 데이터베이스 설계 및 저장 전략

- **데이터베이스**: PostgreSQL (WSL 환경)
- **DB 이름**: `news_db`
- **저장 방식**:
  - 플랫폼별로 원시 테이블 생성
  - `link` 필드에 `UNIQUE` 제약조건 설정
  - 중복 방지를 위해 `ON CONFLICT DO NOTHING` 사용

- **Raw 테이블 스키마 예시**:

```sql
-- BBC
CREATE TABLE IF NOT EXISTS news_bbc_raw (
    id SERIAL PRIMARY KEY,
    title TEXT,
    link TEXT UNIQUE,
    description TEXT,
    pubdate TEXT
);

-- NYT
CREATE TABLE IF NOT EXISTS news_nyt_raw (
    id SERIAL PRIMARY KEY,
    title TEXT,
    link TEXT UNIQUE,
    description TEXT,
    pubdate TEXT,
    creator VARCHAR(100)
);

-- ZDNet Korea
CREATE TABLE IF NOT EXISTS news_zdnet_raw (
    id SERIAL PRIMARY KEY,
    title TEXT,
    link TEXT UNIQUE,
    description TEXT,
    pubdate TEXT,
    author VARCHAR(100)
);

-- Nippon.com
CREATE TABLE IF NOT EXISTS news_nippon_raw (
    id SERIAL PRIMARY KEY,
    title TEXT,
    link TEXT UNIQUE,
    description TEXT,
    pubdate TEXT
);
```

---

## 4. 통합 테이블 설계 및 정제 로직

- **통합 테이블명**: `news_article`
- **스키마**:

```sql
CREATE TABLE news_article (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    writer VARCHAR(255) NOT NULL,
    write_date TIMESTAMP NOT NULL,
    category VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    url VARCHAR(200) UNIQUE NOT NULL,
    keywords JSON DEFAULT '[]'::json,
    embedding VECTOR(1536) NULL
);
```

- **정제 로직 개요**:
  - 각 raw 테이블에서 공통 필드를 SELECT
  - `writer`, `category`가 없으면 `'None'` 문자열로 채움
  - 날짜 포맷 파싱 실패 시 `datetime.now()`로 대체
  - `ON CONFLICT (url) DO NOTHING`으로 중복 삽입 방지

---

## 5. OpenAI API를 통한 추가 처리

### 🔹 5.1 키워드 추출

- **모델**: GPT-4
- **프로세스**:
  - 뉴스 `content`를 OpenAI API로 보내 키워드 5개 추출 요청
  - 응답을 받아 JSON 형태로 변환
  - `keywords` 컬럼에 저장

- **예시 프롬프트**:

```text
"Please extract 5 important keywords from the following news article in a list format: [본문]"
```

### 🔹 5.2 임베딩 생성

- **모델**: `text-embedding-ada-002`
- **프로세스**:
  - 뉴스 `content`를 OpenAI Embedding API로 전송
  - 1536차원 벡터 임베딩을 반환받음
  - `embedding` 컬럼 (pgvector) 형태로 저장

---

## 6. 데이터베이스 업데이트 예시

- **keywords 업데이트**:

```sql
UPDATE news_article
SET keywords = '["AI", "Technology", "News", "Innovation", "Future"]'::json
WHERE id = 1;
```

- **embedding 업데이트**:

```sql
UPDATE news_article
SET embedding = '[0.0123, 0.9876, ...]'::vector
WHERE id = 1;
```

---

## 7. 전체 시스템 흐름 요약

```plaintext
1. RSS 수집 → 
2. Raw 테이블 저장 → 
3. 통합 테이블 정제(news_article) → 
4. OpenAI API 호출 (키워드 추출 + 임베딩 생성) → 
5. news_article 테이블 업데이트 완료
```

---

## 8. 향후 발전 방향

- 키워드 기반 뉴스 카테고리 자동 분류
- pgvector를 활용한 유사 뉴스 추천 기능 구축
- 뉴스 요약 생성 기능 추가 (OpenAI 사용)
- 데이터 수집 파이프라인 자동화 (Cron, Airflow 등)
- Streamlit 또는 Django 기반 시각화 대시보드 개발