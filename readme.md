# 싸피 12기 1학기 Final 관통 Project

## 프로젝트 소개

"SSAFY 12기 관통 파이널 프로젝트 이며, 주제는 금융상품 추천 어플리케이션 입니다. Back-end 기술은 Python, Django, SQLite, Front-end 기술은 Vue, JS 입니다.
주요 기능으로는

- 금융 상품 추천
  - 예, 적금 상품 추천
  - 주식 상품 추천
  - 코인 상품 추천
- 각 상품에 대한 게시글
  - 유저 별로, 각 상품에 대한 코멘트 작성이 가능합니다.
- 유저 게시판
  - 유저 별로, 각 상품에 대한 의견을 나눌 수 있는 게시판입니다.
  - 게시판에는 유저 별로, 코멘트 작성이 가능합니다.

### 주요 기능

1. 로그인, 로그아웃 기능
2. 회원가입 기능
3. 예적금 데이터 (최소 50개 이상)
4. 예적금 상품 조회
5. 예적금 상세 목록 조회
6. 커뮤니티 게시글 기능
7. 커뮤니티 댓글 기능
8. 좋아요 기능 환율 계산 기능
9. 프로필 기능
10. 은행 검색 기능
11. 금융 상품 추천 알고리즘
12. AI 추천 / 검색 서비스 기능
13. 암호화폐 페이지

## 사용 기술

---

### BackEnd

<code><img height="60" src=https://github.com/github/explore/blob/main/topics/django/django.png></code>
<code><img height="60" src=https://github.com/github/explore/blob/main/topics/python/python.png></code>
<code><img height="60" src=https://github.com/github/explore/blob/main/topics/sqlite/sqlite.png></code>

### FrontEnd

<code><img height="60" src=https://github.com/github/explore/blob/main/topics/javascript/javascript.png></code>
<code><img height="60" src=https://upload.wikimedia.org/wikipedia/commons/f/f1/Vue.png></code>
<code><img height="60" src=https://github.com/github/explore/blob/main/topics/html/html.png></code>

### 서비스 설계

- FlowChart, UseCaseDiagram
  - (./images/flowChart.png)
  - (./images/useCase.png)
- ERD
  - ..
- URL 명세서
  - # API Documentation

<details>
<summary>## API 명세서</summary>

### Sign Up

`POST /accounts/signup/`

| Field     | Type    | Required | Description          |
| --------- | ------- | -------- | -------------------- |
| username  | string  | Yes      | 사용자 아이디        |
| email     | string  | Yes      | 이메일 주소          |
| password1 | string  | Yes      | 비밀번호             |
| password2 | string  | Yes      | 비밀번호 확인        |
| age       | integer | No       | 나이                 |
| capital   | integer | No       | 자본금               |
| nickname  | string  | No       | 닉네임 (최대 10자)   |
| sido      | string  | No       | 시/도 (최대 10자)    |
| sigungus  | string  | No       | 시/군/구 (최대 10자) |

### List Articles

`GET /articles/`

**Response:**
| Field | Type | Description |
|-------|------|-------------|
| id | integer | 게시글 ID |
| title | string | 제목 |
| content | string | 내용 |
| create_at | datetime | 작성일 |
| update_at | datetime | 수정일 |
| users | string | 작성자 |

### Create Article

`POST /articles/create/`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | 제목 |
| content | string | Yes | 내용 |

### Article Detail

`GET /articles/<article_pk>/`

**Response:**
| Field | Type | Description |
|-------|------|-------------|
| id | integer | 게시글 ID |
| title | string | 제목 |
| content | string | 내용 |
| users | integer | 작성자 ID |
| create_at | datetime | 작성일 |
| update_at | datetime | 수정일 |
| nickname | string | 작성자 닉네임 |
| comments | array | 댓글 목록 |
| comments_count | integer | 댓글 수 |

### List Products with Options

`GET /financials/financial-products-with-options/`

**Response:**
| Field | Type | Description |
|-------|------|-------------|
| id | integer | 상품 ID |
| options | array | 금융 상품 옵션 목록 |
| fin_product_cd | string | 상품 코드 |
| kor_co_nm | string | 금융사 이름 |
| fin_product_nm | string | 상품명 |

### Financial Comment

`POST /financials/financial-comment_create/<fin_product_pk>/`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| content | string | Yes | 댓글 내용 |

### Exchange Rate

`GET /financials/exchange-rate/`

**Response:**
| Field | Type | Description |
|-------|------|-------------|
| id | integer | 환율 정보 ID |
| cur_unit | string | 통화 단위 |
| cur_nm | string | 통화명 |
| deal_bas_r | string | 매매기준율 |
| bkpr | string | 장부가격 |

</details>
- 컴포넌트 구조도
  - ```
vue-enterprise-boilerplate/
├── docs/
├── generators/
├── jest.config.js
├── package.json
├── package.json.md
├── public/
├── src/
│   ├── App.vue
│   ├── app.config.json
│   ├── app.vue
│   ├── assets/
│   ├── components/
│   │   ├── BankMap.vue
│   │   ├── Calculator.vue
│   │   ├── ChatbotWidget.vue
│   │   ├── CommunityComment.vue
│   │   ├── CryptoCard.vue
│   │   ├── ExchangeCalculator.vue
│   │   ├── ExchangeDetail.vue
│   │   ├── ExchangeItem.vue
│   │   ├── ExchangeList.vue
│   │   ├── FinProductTable.vue
│   │   ├── Footer.vue
│   │   ├── LoginModal.vue
│   │   ├── MainPageBank.vue
│   │   ├── MainPageCarousel.vue
│   │   ├── MainPageTable.vue
│   │   ├── MainProductList.vue
│   │   ├── MiddleNav.vue
│   │   ├── NavBar.vue
│   │   ├── ProductComment.vue
│   │   ├── ProductRecommendOption.vue
│   │   ├── RecommendDep.vue
│   │   ├── RecommendDetail.vue
│   │   └── RecommendSaving.vue
│   ├── plugins/
│   │   └── vuetify.js
│   ├── router/
│   │   ├── index.js
│   │   └── routes.js
│   ├── stores/
│   │   ├── accounts.js
│   │   ├── address.js
│   │   ├── articles.js
│   │   ├── comment.js
│   │   ├── exchange.js
│   │   ├── financial.js
│   │   └── product_comment.js
│   ├── utils/
│   │   └── formatters.js
│   └── views/
│       ├── CommunityDetailView.vue
│       ├── CreateArticleView.vue
│       ├── CryptoView.vue
│       ├── ExchangeView.vue
│       ├── FinView.vue
│       ├── MainView.vue
│       ├── ProductDetailView.vue
│       ├── ProfileView.vue
│       └── SignUpView.vue
├── tests/
└── vue.config.js
```

### 개발기간

- 2024.11.04(월) ~ 2024.11.29(금)
- 업무 분장
- ERD 작성
- API 데이터 준비
- API, ERD에 맞게 Model 관계 설정
- 웹 디자인 작성
- BackEnd 로직 작성
- FrontEnd - BackEnd 통신 및 연결
- 병합
- 발표 및 평가

### 팀원 소개

- **김병년** : 조장, FullStack, Front-end 전체 담당 깃 주소 : https://github.com/KimByeongNyeon/
- **이용재** : FullStack, Back-end 전체 담당 깃 주소 : https://github.com/yongjae730/

### 참고 사항

---

#### API 링크

- 금감원 API
  - 예금 : https://finlife.fss.or.kr/finlife/api/fncCoApi/list.do?menuNo=700052
  - 적금 : https://finlife.fss.or.kr/finlife/api/fdrmEntyApi/list.do?menuNo=700053
- 한국투자증권 API
  - [https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-quotations2#L_07802512-4f49-4486-91b4-1050b6f5dc9d](https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-quotations2#L_a08c3421-e50f-4f24-b1fe-64c12f723c77)
- 코인 API
  - [https://docs.upbit.com/reference/ticker현재가-정보](https://docs.upbit.com/reference/%EC%A0%84%EC%B2%B4-%EA%B3%84%EC%A2%8C-%EC%A1%B0%ED%9A%8C)

#### ERD-Cloud 링크

- https://www.erdcloud.com/d/GdKjjLXs9QvhQZvWz

### 후기
김병년 : 프로젝트 시작 전에 페어를 용재형이랑 하기로 하면서 먼저, 방향성을 완전하게 백, 프론트로 구분하기로 해서 진행했었고, 실제로 코드 작성 시에도 겹치는 부분이 없어서, 단 한번의 충돌 없이 수월하게 프로젝트를 진행했던 것 같습니다. 이번 프로젝트를 하면서, 지금까지 진행했던 프로젝트와는 달리 뭔가 제대로된 기능, 역할의 분리가 된 것 같아서 재밌게 진행했던 것 같고, 프론트엔드 개발자를 희망하는 저로서는 프론트엔드 전반적인 부분을 담당한 것이 제 스스로 성장할 수 있는 계기도 같이 제공 되기도 했고, 실제로 로직을 구성하면서, async, await 와 같은 순서가 보장된 비동기 처리와 같은 기술, 암호화폐 페이지 개발 시에 사용한 WebSocket 기술 등, 여러 가지 기술을 녹여낼 수 있을 만큼 녹여냈다고 생각했고, 더 배울 부분이 많이 남아있다고 느껴졌습니다. 

아쉬웠던 점은, 로직은 금방금방 구성해서 실제 기능에 대한 코딩 시간은 크게 할애하지 않았지만, 자잘한 버그를 잡는 것이 어려웠고, 제가 작성한 코드가 불완전한 코드였다는 것을 다시 알게 되었습니다. 또한, UI/UX 구성 하는 것이 좀 어려웠습니다..
이용재 :