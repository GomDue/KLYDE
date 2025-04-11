import psycopg2
import json
from datetime import datetime
from pathlib import Path

# PostgreSQL 연결 설정
conn = psycopg2.connect(
    host="localhost",
    dbname="news_db",
    user="postgres",
    password="1234",
    port=5432
)
cursor = conn.cursor()

# SELECT 쿼리 실행
cursor.execute("""
    SELECT id, title, writer, write_date, category, content, url, keywords, embedding
    FROM news_article
""")

rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]

# JSON 형태로 변환
result = []
for row in rows:
    row_dict = {}
    for col, val in zip(columns, row):
        # datetime은 문자열로 변환
        if isinstance(val, datetime):
            val = val.isoformat()
        # vector (embedding)은 그대로 두거나 None 처리
        elif isinstance(val, memoryview):  # pgvector가 memoryview로 올 수 있음
            val = list(val.tobytes())  # 또는 base64 등으로 처리 가능
        row_dict[col] = val
    result.append(row_dict)

# 파일로 저장
output_path = Path("./data/news_article_dump.json")
with output_path.open("w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

cursor.close()
conn.close()

print(f"news_article 데이터 저장 완료!")
