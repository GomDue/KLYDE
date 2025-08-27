### KLYDE 데이터 파이프라인 README.md

이 문서는 **KLYDE** 프로젝트의 데이터 파이프라인에 대한 설명을 제공합니다. **Kafka**, **Spark**, **PostgreSQL**을 사용하여 실시간 데이터 처리 및 배치 처리를 수행하고, PostgreSQL과 Elasticsearch 간 데이터 동기화 작업을 자동화합니다. 시스템은 확장 가능하고 유지보수 가능한 구조로 설계되었습니다.


## 1️⃣ **프로젝트 개요**

**KLYDE**는 실시간 뉴스 데이터를 수집하고, 배치 데이터를 분석하여 사용자 맞춤형 뉴스 경험을 제공합니다. 주요 기능은 다음과 같습니다:

* **실시간 뉴스 수집**: **Kafka**를 통해 뉴스 피드를 수집합니다.
* **실시간 데이터 처리**: **Flink**를 사용하여 실시간으로 데이터를 처리하고, **Elasticsearch**와 **PostgreSQL**에 저장합니다.
* **배치 데이터 분석**: **Spark**를 사용하여 배치 데이터를 분석하고, **PDF 리포트**를 생성하여 이메일로 발송합니다.
* **데이터 동기화**: **PostgreSQL**과 **Elasticsearch** 간의 실시간 동기화 작업을 자동화합니다.



## 2️⃣ **디렉토리 구조**

```yaml
pipeline/
├── batch/                                              # 배치 처리 및 데이터 파이프라인 오케스트레이션을 위한 디렉토리
│   ├── dags/                                           # Airflow DAGs 디렉토리
│   │   ├── scripts/                                    # 파이프라인 작업을 위한 Python 스크립트들
│   │   │   ├── postgres_to_elasticsearch_functions.py  # PostgreSQL 데이터를 Elasticsearch로 동기화하는 함수들
│   │   │   └── spark_daily_report.py                   # Spark 기반의 일일 리포트 생성
│   │   ├── daily_report_dag.py                         # 일일 리포트 생성을 위한 Airflow DAG
│   │   └── sync_postgres_to_elasticsearch.py           # PostgreSQL과 Elasticsearch 간 데이터 동기화
│   └── data/                                           # 데이터 및 리포트 파일들
│       ├── news_archive/                               # 아카이브된 뉴스 데이터
│       ├── realtime/                                   # 실시간 데이터 파일들
│       ├── daily_report_20250526.pdf                   # 특정 날짜의 리포트 예시
│       └── daily_report_20250527.pdf
├── docker/                         # Docker 파일
│   ├── Dockerfile.airflow          # Airflow Dockerfike
│   ├── Dockerfile.consumer         # consumer.py Dockerfile
│   ├── Dockerfile.postgre          # PostgreSQL Dockerfile
│   ├── Dockerfile.producer         # producer.py Dockerfile
│   └── Dockerfile.spark            # Spark Dockerfile
│
├── requirements/                   # 의존성 관리 파일들
│   ├── consumer.requirements.txt   # Kafka 소비자 의존성 파일
│   ├── local.requirements.txt      # 로컬 환경 의존성 파일
│   └── producer.requirements.txt   # Kafka 생산자 의존성 파일
├── sql/                            # SQL 관련 파일들
│   └── init.sql                    # 데이터베이스 초기화 SQL 스크립트
├── streaming/                      # 실시간 데이터 처리 관련 파일들
│   ├── config/                     # 실시간 데이터 스트리밍 설정 파일
│   ├── consumer/                   # 실시간 데이터 소비자 관련 코드
│   │   ├── consumer.py             # Kafka 소비자 코드
│   │   ├── models.py               # 데이터 모델 정의
│   │   └── preprocessing.py        # 데이터 전처리 코드
│   └── producer/                   # 실시간 데이터 생산자 관련 코드
│       └── producer.py             # Kafka 생산자 코드
└── README.md                       # 프로젝트 개요 및 설명 파일
```



## 3️⃣ **디렉토리 및 파일 설명**

### **`batch/`**

* **배치 처리 및 데이터 파이프라인 관리**를 위한 디렉토리입니다. 이곳에는 **Airflow DAGs**와 파이프라인 작업을 위한 **Python 스크립트**들이 포함됩니다.

  * **`dags/`**: Airflow DAG 파일들이 포함되어 있으며, 데이터 파이프라인을 스케줄링하고 관리합니다.
  * **`scripts/`**: 데이터 동기화 및 처리 작업을 위한 Python 스크립트들입니다. PostgreSQL과 Elasticsearch 간 데이터 동기화 및 Spark 기반의 일일 리포트 생성 작업을 위한 스크립트가 포함됩니다.
  * **`data/`**: 리포트 및 데이터 파일들이 저장됩니다. 실시간 뉴스 데이터와 배치 처리된 일일 리포트 파일들이 포함됩니다.

### **`docker/`**

* **각 서비스의 Dockerfile**이 포함되어 있는 디렉토리입니다. **Airflow**, **Kafka**, **PostgreSQL**, **Spark** 환경을 설정합니다.

  * **`Dockerfile.airflow`**, **`Dockerfile.consumer`**, **`Dockerfile.producer`**: 각 서비스에 필요한 Docker 환경을 설정합니다.

### **`hdfs/`**

* **HDFS 관련 설정 파일들**이 포함되어 있습니다. HDFS 데이터 노드 초기화 및 시작 스크립트와 설정 파일들이 위치합니다.

  * **`core-site.xml`**, **`hdfs-site.xml`**: HDFS 설정 파일입니다.

### **`requirements/`**

* **Python 의존성 관리 파일들**이 위치한 디렉토리입니다. Kafka 소비자, Kafka 생산자, 로컬 환경에서 필요한 의존성 파일들이 포함되어 있습니다.

### **`sql/`**

* **데이터베이스 초기화 SQL 스크립트**가 포함되어 있습니다. 데이터베이스 구조를 설정하고 초기화하는 데 사용됩니다.

### **`streaming/`**

* **실시간 데이터 처리 관련 코드**가 포함된 디렉토리입니다. Kafka 소비자 및 생산자 코드와 실시간 데이터 스트리밍에 필요한 설정 파일들이 위치합니다.



## 4️⃣ **데이터 흐름**

**KLYDE**의 데이터 파이프라인은 **Kafka**, **Flink**, **Elasticsearch**, **PostgreSQL**, **HDFS**를 포함하는 여러 시스템이 데이터를 실시간으로 처리하고 저장하는 구조로 이루어져 있습니다.

1. **Kafka**에서 실시간으로 뉴스 피드를 수집하고 **Flink**에서 데이터를 처리합니다.
2. 처리된 데이터는 **Elasticsearch**와 **PostgreSQL**에 저장되며, **HDFS**에는 원본 데이터가 날짜별로 저장됩니다.
3. **Spark**는 **HDFS**에 저장된 데이터를 분석하여 일일 리포트를 생성하고 이메일로 발송합니다.


## 5️⃣ **Airflow DAGs**

### 1. **뉴스 데이터 수집 DAG**

* **기능**: 주기적으로 뉴스 피드를 받아 **Kafka**로 전송합니다.
* **작업 흐름**:

  * **Task 1**: `producer.py`를 사용하여 뉴스 RSS 피드를 Kafka에 전송합니다.
  * **Task 2**: 데이터가 Kafka에 성공적으로 전송되면 후속 작업을 진행합니다.

이 구조는 실시간으로 뉴스 데이터를 빠르게 수집할 수 있도록 돕습니다. Kafka가 뉴스 피드를 수집하고 Flink가 이를 실시간으로 처리할 수 있게 전달하므로 최신 정보 반영이 용이합니다. 다만, 뉴스 수집 중 오류가 발생할 수 있기 때문에 오류 처리를 위한 관리가 필요할 수 있습니다.

### 2. **뉴스 데이터 전처리 및 저장 DAG**

* **기능**: **Flink**를 사용하여 실시간으로 데이터를 처리하고 **Elasticsearch**, **PostgreSQL**, **HDFS**에 저장합니다.
* **작업 흐름**:

  * **Task 1**: Kafka에서 데이터를 수신하고 **Flink**에서 전처리합니다.
  * **Task 2**: 전처리된 데이터를 **PostgreSQL**에 저장합니다.
  * **Task 3**: 데이터를 **Elasticsearch**와 **HDFS**에 저장합니다.

이 구조는 실시간 데이터 처리의 장점을 최대한 활용합니다. **Flink**가 데이터를 실시간으로 처리하여 빠르게 분석된 결과를 저장할 수 있도록 하며, **Elasticsearch**와 **PostgreSQL**을 통해 사용자에게 실시간으로 제공되는 뉴스 기사의 품질을 유지합니다. 하지만, 실시간 데이터 처리는 자원 소모가 크므로 시스템 자원의 효율적인 관리가 필요합니다.


## 6️⃣ **파일 저장 경로 및 규칙**

### **HDFS 저장 경로**

* **경로 구조**: 데이터를 날짜별로 파티셔닝하여 저장합니다.
* **예시 경로**: `/data/{날짜}/{URL_HASH}.jsonl`
* **파일명 규칙**: 뉴스 기사의 URL을 해시값으로 변환하여 파일명을 생성합니다. 이를 통해 중복 저장을 방지하고 파일을 효율적으로 관리할 수 있습니다.

### **Elasticsearch 및 PostgreSQL 저장**

* **Elasticsearch**: 뉴스 기사를 빠르게 검색할 수 있도록 인덱싱하여 저장합니다.
* **PostgreSQL**: 뉴스 기사의 메타데이터를 저장하고 대시보드 및 추천 시스템에 사용됩니다.

이 방식은 날짜별로 데이터를 구분하여 효율적으로 관리하며, 중복된 파일이 생성되지 않도록 해시값을 파일명으로 사용합니다. **HDFS**를 통해 대용량 데이터를 분산 저장하면서도 관리가 용이합니다. 하지만, 너무 많은 데이터를 하나의 파일에 저장하면 성능에 영향을 미칠 수 있으므로, 적절한 파일 분할 및 관리가 필요합니다.
