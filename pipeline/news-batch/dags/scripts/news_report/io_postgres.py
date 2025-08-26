from config import *

def load_news_article(spark, start_ts, end_ts):
    query = f"""
        (SELECT
            id, title, writer, write_date, category, content, url, keywords
         FROM {ARTICLES_TABLE}
         WHERE write_date >= TIMESTAMP '{start_ts}'
           AND write_date <= TIMESTAMP '{end_ts}'
        ) AS t
    """
    return (
        spark.read.format("jdbc")
        .option("url", POSTGRESQL_URL)
        .option("dbtable", query)
        .option("user", POSTGRESQL_USER)
        .option("password", POSTGRESQL_PASSWORD)
        .option("driver", JDBC_DRIVER)
        .load()
    )

def load_trend_14d(spark, yester_date_str):
    query = f"""
        (SELECT 
            report_date, total_articles
        FROM {DM_SUMMARY_TABLE}
        WHERE report_date >= DATE '{yester_date_str}' - INTERVAL '14 day'
        ORDER BY report_date
        ) AS t
    """
    return (
        spark.read.format("jdbc")
        .option("url", POSTGRESQL_URL)
        .option("dbtable", query)
        .option("user", POSTGRESQL_USER)
        .option("password", POSTGRESQL_PASSWORD)
        .option("driver", JDBC_DRIVER)
        .load()
        .orderBy("report_date")
    )

def save_df(df, table, mode):
    (
        df.write
        .format("jdbc")
        .option("url", POSTGRESQL_URL)
        .option("dbtable", table)
        .option("user", POSTGRESQL_USER)
        .option("password", POSTGRESQL_PASSWORD)
        .option("driver", JDBC_DRIVER)
        .mode(mode)
        .save()
    )

