# SSAFY 맞춤형 뉴스 데이터 파이프라인 환경 설정 관통 PJT(1) 가이드 정리

## 최종 목표
[Extract]                   [Transform]             [Load]
Kafka Topic  →  Flink  →  데이터 처리/변환   →  PostgreSQL(DB 저장)
(JSON or RSS) (스트리밍)  (카테고리 분류)    →  Elasticsearch(검색)
                  │        (키워드 추출)      
                  │        (벡터 임베딩)
                  │
                  ↓            
                HDFS  →  Spark  →  리포트 생성  →  HDFS 아카이브
              (임시저장)  (배치)     (pdf)          (장기 보관)

> **목차 (원본 README의 목차와 실제 내용의 순서를 모두 반영함)**
>
> 1. PostgreSQL 설치 및 설정
> 2. 필요한 라이브러리 설치

---

## 1. PostgreSQL 설치 및 설정

### 1.1. PostgreSQL 설치 (Linux - Ubuntu)

1. **PostgreSQL 설치**  
   터미널에서 아래 명령어를 실행하여 PostgreSQL과 추가 패키지를 설치합니다.

   ```bash
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib
   ```

2. **서비스 상태 확인**  
   PostgreSQL 서비스가 정상 실행 중인지 확인합니다.

   ```bash
   sudo service postgresql status
   ```

### 1.2. PostgreSQL 데이터베이스 설정

1. **PostgreSQL 접속**  
   기본 사용자 `postgres`로 전환한 후 `psql` 셸에 접속합니다.
   PostgreSQL 설치 시 만들어지는 **기본 PostgreSQL 사용자 postgres**는 리눅스의 postgres 계정으로만 접속이 허용되어 있음

   ```bash
   sudo -i -u postgres
   psql
   ```

2. **데이터베이스 생성**  
   `news` 데이터베이스를 생성합니다.

   ```sql
   CREATE DATABASE news;
   ```

3. **사용자 생성 및 권한 부여**  
   SSAFY 전용 사용자 `ssafyuser`를 생성하고, `news` 데이터베이스에 대한 모든 권한을 부여합니다.

   ```sql
   CREATE USER ssafyuser WITH PASSWORD 'ssafy';
   GRANT ALL PRIVILEGES ON DATABASE news TO ssafyuser;
   ```

sudo vi /etc/postgresql/16/main/pg_hba.conf

# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5

4. **테이블 생성**

   1. **데이터베이스 변경**  
      생성한 `news` 데이터베이스로 접속합니다.

      ```bash
      \c news
      ```

   2. **pgvector 확장 설치 (최초 한 번 실행) 및 테이블 생성**  
      아래 SQL 명령어를 실행하여 `pgvector` 확장을 설치하고, `news_article` 테이블을 생성합니다.

      ```sql
      -- pgvector 확장이 필요한 경우 (최초 한 번만 실행)
      CREATE EXTENSION IF NOT EXISTS vector;

      -- news_article 테이블 생성
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
 # 이후에는 NOT NULL쓸 것
   exit을 통해 터미널을 나올 수 있습니다.


-- 5. 권한 부여
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO ssafyuser;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON SEQUENCES TO ssafyuser;
GRANT CREATE ON SCHEMA public TO ssafyuser;



## 2. 필요한 라이브러리 설치
python3.11 -m venv ~/venvs/pjt
source ~/venvs/pjt/bin/activate

pip install -r requirements.txt

---

## 마무리

위의 단계들을 차례대로 진행하고 rss의 news를 잘 수집하고 저장하는 것이 목표입니다. 
이를 시작으로 이후 SSAFY 맞춤형 뉴스 데이터 파이프라인 환경을 지속적으로 개발하며 PostgreSQL, Hadoop, Kafka, Airflow, elasticsearch를 이용해 성공적으로 프로젝트를 구축하는 과정을 거치게 됩니다.