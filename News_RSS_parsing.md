# 📘 뉴스 RSS 기반 통합 데이터베이스 구축 프로젝트

## 1. 프로젝트 개요

본 프로젝트는 **BBC, 뉴욕타임즈(NYT), Nippon.com, ZDNet Korea** 등 다양한 뉴스 플랫폼의 RSS 피드를 기반으로,  
**뉴스 데이터를 실시간으로 수집, 정제, 통합**하는 데이터 파이프라인을 구축하는 것을 목표로 한다.  
수집된 뉴스는 **플랫폼별 원시 테이블**에 저장되고, 이후 통합 정제 과정을 통해 **분석용 통합 테이블(`news_article`)**로 병합되어  
향후 키워드 분석, 뉴스 임베딩, 유사 뉴스 검색 등 고급 분석으로 확장 가능한 구조를 설계하였다.

---

## 2. 데이터 수집 구조

- **수집 대상 플랫폼**: BBC, NYT, Nippon.com, ZDNet Korea  
- **사용 도구**: Python + feedparser + psycopg2 + dateutil  
- 각 플랫폼의 RSS 피드를 파싱하여 뉴스 항목의 `title`, `link`, `description`, `published date`, `author` 등을 추출  
- 추출된 뉴스는 PostgreSQL에 저장되며, 각 플랫폼별로 다음 테이블을 사용:
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

---

## 4. 통합 테이블 설계 및 정제 로직

- **테이블명**: `news_article`
- **주요 필드**:
  - `title`, `writer`, `write_date`, `category`, `content`, `url`
  - 확장 필드: `keywords` (JSON), `embedding` (VECTOR 1536)
- **정제 로직**:
  - 각 raw 테이블에서 공통 필드를 SELECT
  - `writer`, `category`가 없으면 `'None'`으로 채움
  - 날짜 포맷 파싱 실패 시 `datetime.now()`로 대체
  - `ON CONFLICT (url) DO NOTHING`으로 중복 방지 삽입

---

## 5. 향후 확장 방향

- **키워드 추출 및 태깅**: `content`에서 주요 키워드 추출 → `keywords`에 저장
- **뉴스 임베딩 적용**: OpenAI, KoBERT 등으로 벡터화 → `embedding`에 저장
- **벡터 기반 유사 뉴스 검색**: `pgvector` 확장을 활용한 검색 기능 구현
- **자동화 수집 파이프라인**:
  - cron, Airflow, Kafka 등을 활용한 정기 수집 자동화
- **웹 기반 시각화 대시보드**:
  - Streamlit, Django 등을 활용한 트렌드 분석 웹 앱 구축
