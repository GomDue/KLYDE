# 프로젝트 개요

이 프로젝트는 Apache Kafka, Spark, PostgreSQL을 사용하여 실시간 데이터 처리 및 배치 처리를 수행합니다. 또한 PostgreSQL과 Elasticsearch 간 데이터 동기화 작업을 자동화하고, 다양한 시스템을 통합하여 확장성 있고 유지보수 가능한 구조로 설계되었습니다.

## 디렉토리 구조

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
├── hdfs/                           # HDFS 관련 파일들
│   ├── config/                     # HDFS 설정 파일들
│   │   ├── core-site.xml           # HDFS core-site 설정
│   │   ├── hdfs-site.xml           # HDFS site 설정
│   │   ├── mapred-site.xml         # MapReduce 설정
│   │   └── yarn-site.xml           # YARN 설정
│   ├── init-datanode.sh            # HDFS 데이터노드 초기화 스크립트
│   └── start-hdfs.sh               # HDFS 시작 스크립트
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

### 디렉토리 및 파일 설명

* **`batch/`**
  배치 처리 및 데이터 파이프라인을 관리하는 디렉토리입니다. 주로 Airflow DAGs와 파이프라인 작업을 위한 Python 스크립트들이 위치합니다.

  * **`dags/`**: Airflow DAG 파일들이 위치한 디렉토리로, 주로 데이터 파이프라인의 스케줄링 및 관리에 사용됩니다.
  * **`scripts/`**: 데이터 처리와 동기화 작업을 위한 Python 스크립트들이 포함됩니다. PostgreSQL에서 Elasticsearch로 데이터를 동기화하거나, Spark 기반의 리포트를 생성하는 스크립트가 있습니다.
  * **`data/`**: 리포트 및 데이터 파일이 저장된 디렉토리로, 아카이브된 뉴스 데이터 및 실시간 데이터 파일이 포함됩니다.

* **`docker/`**
  프로젝트에서 사용하는 각 서비스에 대한 Dockerfile들이 포함되어 있는 디렉토리입니다. 각 서비스(예: Airflow, Kafka 소비자/생산자, PostgreSQL, Spark) 환경을 설정하는 파일들이 위치합니다.

* **`hdfs/`**
  HDFS 관련 파일들이 저장된 디렉토리입니다. HDFS 데이터 노드 초기화 및 시작을 위한 스크립트와 설정 파일들이 포함되어 있습니다.

* **`requirements/`**
  프로젝트에서 필요한 Python 의존성 관리 파일들이 위치한 디렉토리입니다. Kafka 소비자, 로컬 환경, Kafka 생산자에 대한 의존성 파일이 있습니다.

* **`sql/`**
  데이터베이스 초기화 및 관련 SQL 스크립트가 저장된 디렉토리입니다. `init.sql` 파일을 통해 데이터베이스 스키마 및 초기화 작업을 처리합니다.

* **`streaming/`**
  실시간 데이터 스트리밍을 위한 코드가 포함된 디렉토리입니다. Kafka 소비자 및 생산자 코드, 그리고 실시간 데이터 처리와 관련된 설정 파일들이 위치합니다.

  * **`consumer/`**: Kafka 소비자 관련 코드가 포함된 디렉토리로, 데이터 소비 및 모델을 처리하는 코드가 들어 있습니다.
  * **`producer/`**: Kafka 생산자 관련 코드가 포함된 디렉토리로, 데이터를 Kafka로 전송하는 코드가 포함되어 있습니다.
