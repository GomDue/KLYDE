# SSAFY AI 뉴스 큐레이션 플랫폼

AI 기반의 맞춤형 뉴스 추천 및 검색 플랫폼입니다. 사용자는 카테고리별 뉴스를 탐색하거나 키워드로 직접 검색할 수 있으며, 뉴스에 좋아요를 남겨 개인화된 추천이 가능하도록 설계되어 있습니다.

---

## 🔧 기술 스택

### 🖥️ Frontend (Vue 3)
- Vite + Vue 3 Composition API
- SCSS + Scoped CSS 모듈
- Axios로 비동기 API 연동
- 컴포넌트 기반 설계: `NewsCard.vue`, `NewsView.vue`, `NewsSearchView.vue`, `PaginationButton.vue` 등

### 🛠️ Backend (Django REST Framework)
- Django 4.x
- Django REST Framework
- PostgreSQL
- 사용자 모델 커스터마이징 (`users.User`)
- 뉴스 모델 `Article` 구현
- 좋아요 기능 (ManyToManyField)
- 필터링, 정렬, 검색, 페이지네이션 지원

---

## 📦 기능 요약

### ✅ 메인 뉴스 목록 (NewsView.vue)
- 카테고리별 탭 필터링 (정적 탭 목록 기반)
- 최신순 / 추천순 정렬 옵션
- 페이지네이션 구현
- `NewsCard.vue`를 활용한 기사 카드 UI

### ✅ 뉴스 검색 (NewsSearchView.vue)
- 입력된 키워드로 제목 필터링
- 검색 버튼 또는 `Enter` 키로 실행
- 결과 없을 경우 메시지 출력
- 기사 카드 형태로 동일하게 출력 (`NewsCard.vue` 재사용)
- 공백 입력 시 오류 메시지 출력

### ✅ 좋아요 기능
- 로그인한 사용자만 좋아요 가능
- 하트 버튼 클릭 시 실시간 토글
- 좋아요 수 UI 반영
- 추천순 정렬에 반영

---

## 🗂️ API 명세

### `/news-list/`
- `GET`
- Query Parameters:
  - `category`: 카테고리 이름
  - `page`: 페이지 번호
  - `limit`: 페이지당 기사 수
  - `sort_by`: `'latest'` 또는 `'recommend'`

### `/news/like/`
- `POST`: 좋아요 추가/삭제 토글
- Body: `{ article_id: number }`
- 인증 필요

### `/news/{id}/`
- `GET`: 단일 기사 상세 조회

---

## 🧪 예시 데이터 모델

```json
{
  "id": 12,
  "title": "AI가 추천한 오늘의 뉴스",
  "writer": "unknown",
  "write_date": "2025-05-02T08:00:00Z",
  "category": "정치",
  "content": "오늘은 AI가 추천한 정치 뉴스입니다.",
  "url": "https://example.com/article/12",
  "keywords": ["AI", "정치", "추천"],
  "article_interaction": {
    "likes": 3,
    "read": 102
  },
  "is_liked": true
}
```

## 🛠️ 기술 구성 및 역할 분담

### 🖼 Frontend (Vue 3)
- `NewsView.vue`: 탭별 뉴스 추천 및 정렬(최신순/추천순) 기능 구현
- `NewsSearchView.vue`: 전체 뉴스에서 제목 키워드 검색 기능 구현 (엔터 및 버튼 기반 검색)
- `NewsCard.vue`: 뉴스 카드 컴포넌트로 제목, 본문 요약, 날짜, 카테고리, 좋아요 토글, 해시태그 키워드 표시
- `StateButton.vue`, `ContentBox.vue`, `PaginationButton.vue`: 상태 선택, 카드 레이아웃, 페이지네이션 UI 공통 컴포넌트

### 🌐 Backend (Django REST Framework)
- `/news-list/`: 뉴스 목록 API. 카테고리 필터링 및 정렬, 페이지네이션 지원
- `/news/<id>/`: 상세 뉴스 조회 API. 조회수 자동 증가 처리 포함
- `/news/like/`: 뉴스 좋아요 토글 API. 프론트에서 토글 시 실시간 반영되도록 처리
- `Article`, `User`: 좋아요 다대다 관계 설정, 사용자 기반 좋아요 체크
- `ArticleSerializer`: 클라이언트에 필요한 데이터 필드 구성
