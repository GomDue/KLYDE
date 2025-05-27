# 📰 KLYDE - Personalized AI News Curation Platform

## 1. 🔍 프로젝트 개요

**KLYDE**는 *Clarity* + *Glide*의 합성어로, 사용자 맞춤 뉴스를 귀러하게 추천하는 AI 기반 플랫폼입니다.
실시간 뉴스 수집, 해외 참고, 대신기능, 책보트 구조 까지 가장하며, 다양한 행동을 제공합니다.

---

## 2. 🧹 전체 시스템 구조

```
DATA-TRACK-PJT/
├── DATA-TRACK-PJT-FRONT/       # Vue 기반 프러티언드 (localhost:3000)
├── DATA-TRACK-PJT-BACK/        # Django 기반 백엔드 (localhost:8000)
├── docker-compose.yaml         # Kafka, Flink, Airflow 등 통합 구성
```

---

## 3. 🌟 주요 기능

* 실시간 뉴스 수집 및 전처리 (Kafka + Flink)
* 개인 관심 기본 뉴스 추천 & 대신보 시각화
* 게시 좋아요, 조회수, 댓글 기능
* GPT-4o-mini 기반 AI 뉴스 책보트 (LangChain)
* JWT 인증 기본 로그인/회원가입
* 뉴스 검색, 정렬, 티넷 개인적 UX 건설

---

## 4. 🛠 기술 스택

### 💻 Frontend (Vue.js)

* Vue 3 (Composition API), Vite
* Axios, Pinia, Chart.js
* 실행 주소: [http://localhost:3000](http://localhost:3000)

### 🖙 Backend (Django)

* Django REST Framework
* PostgreSQL, Celery, Redis
* LangChain, OpenAI GPT API
* 실행 주소: [http://localhost:8000](http://localhost:8000)

### 🔀 Streaming & Infra

* Apache Kafka, Apache Flink (PyFlink)
* Airflow (batch/DAG 관리 예정)
* Docker / Docker Compose
* Elasticsearch (뉴스 유사도 분석, 통합 예정)

---

## 5. ⚙️ 실행 방법

### ✅ 1. 프러티언드 실행

```bash
cd DATA-TRACK-PJT-FRONT
npm install
npm run dev
# → http://localhost:3000
```

### ✅ 2. 백엔드 실행

```bash
cd DATA-TRACK-PJT-BACK
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# → http://localhost:8000
```

### ✅ 3. 도커 기반 Kafka/Flink 시스템 실행

```bash
cd DATA-TRACK-PJT
docker-compose up --build
# Kafka, Zookeeper, Flink, Airflow, ElasticSearch 등 시작
```

---

## 6. 📂 주요 디렉터리 설명

### 📁 DATA-TRACK-PJT-FRONT

* `src/api`: Axios 기반 API 통신 모듈
* `src/components`: 공통 UI 컴포넌트
* `src/views`: Main, Detail, Settings, Auth 페이지
* `src/stores`: Pinia 상태 관리
* `src/composables`: 공통 커스텀 훅 (hook)

### 📁 DATA-TRACK-PJT-BACK

* `news`: 뉴스 목록, 크롤링, 추천 알고리즘
* `users`: 사용자 JWT 인증, 프리평
* `chat`: 챗봇 모듈 (LangChain + GPT)
* `dashboard`: 사용자 관심 키워드 및 행동 추적

### 📁 DATA-TRACK-PJT (infra)

* `docker/`: Kafka, Flink, PostgreSQL 구성
* `sql/init.sql`: 첫 시 DB 스키마 생성
* `streaming/`: Kafka → Flink → PostgreSQL 파이피노
* `batch/`: (Airflow 기본 DAG 구성 예정)

---

## 7. 🧐 아키텍처 요약

```
[RSS 뉴스 수집]
      ↓
Kafka Producer → Kafka Topic → Flink Consumer → PostgreSQL
                                        └ Elasticsearch 유사 뉴스 (현재 계획 중)
```

---

## 8. 💬 챗봇 시스템

* 자기소개서 / 기업 정보 / 최근 뉴스 Embedding
* LangChain PromptTemplate 구성
* GPT-4o-mini 기반 뉴스 문의 참조 & 응답
