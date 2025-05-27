# 🧠 KLYDE Backend Features

## 1. 프로젝트 앱 구조 및 역할

| 앱 이름        | 설명                                      |
| ----------- | --------------------------------------- |
| `chat`      | GPT-4o-mini 기반 뉴스 챗봇. 기사 요약/질문/번역 기능 포함 |
| `dashboard` | 유저의 활동 이력(좋아요, 조회수) 기반 대시보드 분석 기능       |
| `news`      | 기사 데이터 관리, 필터링, 추천, 댓글 등 핵심 콘텐츠 API     |
| `users`     | 회원가입, 로그인, 유저 정보, JWT 인증, 이메일 수신 설정 등   |

---

## 2. `chat` 앱 상세 기능

### 🧠 뉴스 챗봇 기능 (LangChain + GPT)

* **API**: `POST /api/chat/`
* **인증**: 로그인 필수 (`IsAuthenticated`)
* **입력**: `article_id`, `question`
* **출력**: 해당 뉴스 기반 GPT 응답

### 🤖 사용 모델 및 구성

* **모델**: `gpt-4o-mini`
* **LangChain** 구성:

  * `ChatOpenAI`
  * `ChatPromptTemplate`
  * `SystemMessage`, `HumanMessage`, `AIMessage`

### 💬 시스템 프롬프트 예시

```text
You are Newsie, a multilingual and friendly AI assistant who helps users understand news articles.
You can answer questions about the article, summarize it, extract keywords, and translate it into Korean if requested.
You can also understand and respond to questions written in Korean.
If the question is not about this article at all (e.g., about cooking or movies), then respond with:
"Sorry, I couldn't find that information in this article."

### Title: {article.title}
### Date: {article.write_date}
### Content: {truncate_text(article.content)}
```

### 💾 히스토리 관리

* Django 세션을 통해 `chat_history_{article_id}` 형식으로 대화 히스토리 저장 및 불러오기
* 직렬화 가능하도록 `user`, `bot` 형태로 저장함

---

## 3. `dashboard` 앱 상세 기능

### 📊 사용자 대시보드 통계 API

* **API**: `GET /api/dashboard/`
* **인증**: 로그인 필수 (`IsAuthenticated`)
* **기능**:

  * 사용자가 **좋아요 누른 기사 목록** 조회
  * 최근 7일간 **기사 조회 수 통계**
  * 좋아요한 기사 기반 **카테고리 분포**
  * 좋아요한 기사 기반 **키워드 빈도수 (Top 5)**

### 🧱 모델 구성

```python
class UserReadArticle(models.Model):
    user = ForeignKey(User)
    article = ForeignKey(Article)
    read_at = DateTimeField(auto_now_add=True)

class UserLikedArticle(models.Model):
    user = ForeignKey(User)
    article = ForeignKey(Article)
    liked_at = DateTimeField(auto_now_add=True)
```

### 📦 반환 JSON 예시

```json
{
  "category_stats": {"경제": 4, "정치": 2},
  "keyword_stats": {"인플레이션": 3, "금리": 2},
  "read_by_day": {"2024-05-21": 2, "2024-05-22": 4},
  "liked_articles": [
    {"id": 12, "title": "한국은행 금리 동결", "author": "홍길동", "write_date": "2024-05-21"}
  ]
}
```

---

## 4. `news` 앱 상세 기능

### 📰 기사 관련 기능

* `GET /api/news/`: 카테고리 + 추천순/최신순 정렬된 기사 목록 조회
* `GET /api/news/<id>/`: 기사 상세 정보 + 유사 기사 포함 반환
* `GET /api/news/search/`: Elasticsearch 기반 검색
* `POST /api/news/read/<id>/`: 조회수 1 증가 및 기록 저장
* `POST /api/news/like/`: 좋아요 토글 처리
* `GET /api/news/like/?article_id=...`: 좋아요 여부 조회
* `GET /api/news/similar/<id>/`: 유사 기사 5개 반환 (pgvector 기반)
* `GET /api/news/recommend/`: 사용자 프로필 기반 추천 기사 반환

### 💬 댓글 기능

* `GET /api/comments/?article_id=...`: 댓글 리스트 반환
* `POST /api/comments/`: 댓글 생성
* `PUT /api/comments/<id>/`: 댓글 수정
* `DELETE /api/comments/<id>/`: 댓글 삭제 (작성자 본인만 가능)

### 🧠 관련 기술

* `VectorField`: pgvector 기반 임베딩 유사도 계산
* `CosineDistance`: 유사 기사 및 추천 기사 계산 시 사용
* Elasticsearch: 빠른 키워드/내용 기반 검색 구현

---

## 5. `users` 앱 상세 기능

### 👤 사용자 모델 및 인증

* 커스텀 `User` 모델 사용

  * 기본 `username` 필드 제거, `email` 기반 로그인
  * `email_consent` 필드로 이메일 수신 동의 여부 저장
* **사용자 인증 방식**: JWT (SimpleJWT)

### 🧾 API 기능 요약

| 기능           | 메서드          | 경로                            | 설명                   |
| ------------ | ------------ | ----------------------------- | -------------------- |
| 사용자 로그인      | `POST`       | `/api/users/login/`           | 이메일/비밀번호 인증 및 JWT 발급 |
| 사용자 정보 조회    | `GET`/`POST` | `/api/users/info/`            | 현재 로그인된 사용자 정보 반환    |
| 비밀번호 변경      | `POST`       | `/api/users/change-password/` | 현재/새 비밀번호 입력 후 변경    |
| 계정 삭제        | `DELETE`     | `/api/users/delete/`          | 로그인된 계정 삭제           |
| 이메일 수신 동의 변경 | `PATCH`      | `/api/users/email-consent/`   | 이메일 수신 여부 업데이트       |

### 📧 이메일 기반 기능

* `email_consent=True` 설정된 사용자에게만 **Airflow에서 정기 뉴스 분석 리포트 이메일 발송**
* 향후 뉴스 기반 알림 서비스 등 확장 가능

### 🧱 주요 모델

```python
class User(AbstractUser):
    username = None
    email = EmailField(unique=True)
    email_consent = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
```

---

## ⚙️ 프로젝트 전역 설정 요약 (settings.py)

### 🔐 인증 및 사용자 설정

* `AUTH_USER_MODEL = 'users.User'`: 커스텀 유저 모델 사용 (username 제거, email 기반)
* `ACCOUNT_USERNAME_REQUIRED = False`, `ACCOUNT_AUTHENTICATION_METHOD = "email"`, `ACCOUNT_EMAIL_REQUIRED = True`: 이메일 기반 인증 및 중복 방지 설정
* `ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"`: username 없는 회원가입 오류 방지용 어댑터 지정 (필요시 커스터마이징 가능)

### 🔑 JWT 인증

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}
```

### 💬 세션 설정

* `SESSION_ENGINE = "django.contrib.sessions.backends.db"`: LangChain 챗봇 세션 관리 기반 설정

### 🌐 CORS 설정

* 개발 환경에서는 `CORS_ALLOW_ALL_ORIGINS = True`로 설정
* 운영 환경에서는 아래처럼 제한 권장:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://your-production-domain.com",
]
```

### 📧 이메일 발송 설정 (Airflow와 연동 시)

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
```

* 이메일 기반 뉴스 리포트 전송 등에 활용됨

### 🌿 기타

* `dotenv`를 사용해 환경변수 로딩: `load_dotenv()` + `.env` 파일
* `REST_AUTH`, `dj_rest_auth`, `allauth` 기반 인증 흐름 구성

---
