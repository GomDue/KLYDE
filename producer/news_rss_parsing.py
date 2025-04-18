import psycopg2
from datetime import datetime

# 연결 설정
conn = psycopg2.connect(
    host="localhost",
    dbname="news",
    user="postgres",
    password="1234",
    port=5432
)
cursor = conn.cursor()

# 통합 대상 테이블들
tables = [
    ("news_bbc_raw", "title", "link", "description", "pubdate", None, None),
    ("news_nyt_raw", "title", "link", "description", "pubdate", "creator", None),
    ("news_zdnet_raw", "title", "link", "description", "pubdate", "author", None),
    ("news_nippon_raw", "title", "link", "description", "pubdate", None, None)
]

# 테이블마다 SELECT해서 news_article로 INSERT
for tbl, title_col, url_col, content_col, date_col, writer_col, category_col in tables:
    writer_expr = f"'None'" if writer_col is None else f"COALESCE({writer_col}, 'None')"
    category_expr = f"'None'" if category_col is None else f"COALESCE({category_col}, 'None')"

    query = f"""
        SELECT {title_col}, {url_col}, {content_col}, {date_col},
               {writer_expr} AS writer, {category_expr} AS category
        FROM {tbl}
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        title, url, content, date_str, writer, category = row
        try:
            write_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z') if date_str else datetime.now()
        except:
            write_date = datetime.now()

        cursor.execute("""
            INSERT INTO news_article (title, writer, write_date, category, content, url)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING;
        """, (title, writer, write_date, category, content, url))

conn.commit()
cursor.close()
conn.close()

print("news_article 테이블 통합 완료!")
