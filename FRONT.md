# 🔄 KLYDE Frontend Features

> 프러티언드 파일 구조가 `DATA-TRACK-PJT-FRONT` 폴더에 위치해 있는 Vue 3 Composition API 구성의 프로젝트입니다.

## 프로젝트 주요 다음의 활성 페이지와 각 요소 설명

---

### 1. 🏠 LandingView\.vue

* 첫 번째 로드시 등장하는 페이지
* **KLYDE 로고** 가중점 표시, 로그인 / 회원가입 버튼 모드

<p align="center">
  <img src="./public/assets/landing-page.gif" width="500" alt="Landing Page GIF" />
</p>

### 2. 👤 LoginView\.vue / RegisterView\.vue

* JWT 기반 로그인 / 회원가입 창
* 성공 후 **NewsView\.vue** 로 리뷰터 redirect

### 3. 📰 NewsView\.vue (Main page)

* 현재는 회원 로그인 후 처음 보게되는 메인 페이지
* 개인 관심 **키워드 필터**로 게시 찾기
* **ElasticSearch 가지고 검색** 가능
* **10개 가이스를 페이지다 보기**, 날짜순 / 추천순 정렬 가능

<p align="center">
  <img src="./public/assets/newsview-dashboard-settings.gif" width="500" alt="전체 페이지 탐색 GIF" />
</p>

<p align="center">
  <img src="./public/assets/search-sort.gif" width="500" alt="검색 및 정렬 기능 GIF" />
</p>

### 4. 📃 NewsDetailView\.vue

* 게시 클릭시 **전문 보기 페이지**로 이동
* 용어구 표시, 글 평가 및 **5개의 관련 글 사이드바** 구성
* 하드 클릭으로 나오는 **댓글 작성/표시 구조**
* 가장 아래 원거에 **AI 책보트 조회/번역 가능**

<p align="center">
  <img src="./public/assets/news-detail-comment.gif" width="500" alt="뉴스 상세 및 댓글 기능 GIF" />
</p>

### 5. 📊 DashBoardView\.vue

* 사용자가 **읽어보고** `목록을 추적`한 것과, 관심가 있던 게시에 대해
* **가이 참가에 가까운 차포\uud2b8 구성 (Chart.js)**

### 6. ⚙ SettingsView\.vue

* 비밀번호 변경
* 계정 삭제 (개인 정보 삭제 API)
* 이메일 수신 동의 설정

### 7. 🔔 TheHeader.vue & TheFooter.vue

* 각 페이지에 다룰기 위한 router-link
* Header: `News`, `Dashboard`, `Settings`, `Logout`
* Footer: 보조 정보 표시, 가능성 예정

### 8. 🛈 ChatBotLauncher.vue / ChatBotPopup.vue

* 가장 원하는 뉴스에 대해
* 개인적 **보조 문의 (LangChain + GPT)** 가능
* 처리: 보기/번역/회곡 요청 형식 등

<p align="center">
  <img src="./public/assets/chatbot.gif" width="500" alt="챗봇 기능 GIF" />
</p>

---

## 패시지는 어느 요소가?

* `PaginationButton.vue`: 뉴스 목록의 페이지다 표시/나누기
* `NewsCard.vue`, `BoardCard.vue`: 게시 목록 포함조 콘텐츠
* `ContentBox.vue`: 뉴스 변수적 요소 개요 보조

---

## 함수/콘텐츠 구성

* `useDate.js`, `useValidation.js`: 공통 데이터 형식 처리, 입력 검증
* `api/*.js`: axios 보조로 다룰 목록 (news, comment, dashboard, user, chatbot)

---

이와 같이 각 페이지가 매우 명확한 기능 만성 방식을 가진…
KLYDE의 Vue.js 기반 frontend 개발 구조입니다. 더 복잡해지면 다시 정보를 바탕해서 다시 추가해줄게!
