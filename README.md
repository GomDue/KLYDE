# 📰 **KLYDE - Personalized AI News Curation Platform**

> 실시간 뉴스와 인사이트를 한눈에 \
> Clarity + Glide → 명확하고 매끄럽게 뉴스를 탐색하는 AI 기반 플랫폼

## 1️⃣ **프로젝트 개요**

KLYDE는 실시간 뉴스 수집, 추천, 요약/번역 기능을 제공하는 **AI 뉴스 플랫폼**입니다.

### 주요 문제 해결 목표

* **뉴스 탐색의 어려움**: 방대한 뉴스 속에서 맞춤형 뉴스 쉽게 찾기.
* **복잡한 정보 처리**: 뉴스 기사 요약 및 번역으로 사용자 이해 지원.
* **맞춤형 뉴스 제공**: 사용자의 관심사에 맞춘 개인화된 뉴스 추천.

## 2️⃣ **주요 기능**

### 1. **맞춤형 뉴스 제공**

* **AI 추천 시스템**으로 사용자의 관심사 분석 후 맞춤형 뉴스 피드를 실시간 제공.
* **카테고리 및 키워드 기반**으로 뉴스 추천.

### 2. **AI 챗봇**

* **뉴스 요약**, **키워드 추출**, **번역**을 제공하는 AI 챗봇.
* **LangChain**을 이용해 프롬프트 동적 구성 및 정교한 질의 처리.

### 3. **대시보드**

* **뉴스 소비** 데이터를 시각화하여 사용자의 열람 기록, 좋아요, 시청 횟수 분석.
* **개인화된 뉴스 피드**와 **핵심 키워드** 기반 대시보드 제공.

### 4. **댓글 작성 및 관련 뉴스 탐색**

* 기사에 **댓글 작성** 및 다른 사용자의 의견과 상호작용.
* **관련 뉴스 탐색**으로 더 많은 정보를 제공.


## 3️⃣ **기술 스택**

| 영역     | 기술                             | 역할                                        |
| ------ | ------------------------------ | ----------------------------------------- |
| 실시간 수집 | Kafka, BeautifulSoup, Selenium | RSS/웹 크롤링 후 Kafka로 뉴스 스트리밍                |
| 실시간 처리 | Kafka Producer/Consumer        | 기사 전처리 후 PostgreSQL 저장 & Elasticsearch 색인 |
| 배치 분석  | Spark, Airflow, Matplotlib     | 전일 데이터 집계·시각화 → PDF 리포트 자동 발송 (Gmail API) |
| 저장소    | PostgreSQL, Elasticsearch      | 정합성 보장(DB) & 고속 검색(ES)                    |
| 웹      | Django (BE), Vue.js (FE)       | 인증, API 제공, 대시보드 시각화                      |
| AI     | GPT-4o-mini, LangChain         | 요약·번역·키워드 추출·카테고리 분류                      |
| 인프라    | Docker Compose                 | 통합 개발 환경 및 서비스 컨테이너 관리                    |


## 4️⃣ **시스템 아키텍처**

**KLYDE**의 데이터 흐름 및 구성 요소 간 관계는 아래의 시스템 아키텍처 다이어그램에서 확인할 수 있습니다.

![System Architecture](public/assets/system_architecture.png)

* Batch와 Streaming에 대한 Data Flow는 `pipeline\`의 README.md에 있습니다.

## 5️⃣ **ERD (Entity Relationship Diagram)**

![ERD Diagram](public/assets/ERD.png)


## 6️⃣ **프로젝트 구조**

```mk
project/
├── backend/      # Django (auth, news, users, dashboard, chat)
├── frontend/     # Vue.js (UI, 대시보드, 정적 파일)
├── pipeline/     # Data pipeline (Airflow, Spark, Kafka, SQL)
├── public/       # 다이어그램/이미지
└── README.md
```


## 7️⃣ **API**

7) 주요 API
* Auth: POST /api/auth/login, POST /api/auth/register
* Articles: GET /api/articles, GET /api/articles/{id}
* Comments: POST /api/comments, GET /api/comments/{article_id}
* Chatbot: POST /api/chat (요약·번역·키워드)
* Dashboard: GET /api/dashboard


## 8️⃣ **향후 개선 방향**

1. **Elasticsearch 검색 품질 개선**: 문맥 기반 유사도 검색 및 정렬 고도화.
2. **추천 시스템의 개인화 개선**: 클릭 시간, 조회 이력 등 사용자 행동 데이터 반영.
3. **대시보드 시각화 개선**: 직관적 UI 및 반응형 대시보드 개선.
4. **서버 측 페이지네이션**: 현재 방식에서 서버 측 페이지네이션으로 개선.
