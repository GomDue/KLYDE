import json
from loguru import logger

from pyspark.sql import SparkSession
from pyspark.sql.types import ArrayType, StringType
from pyspark.sql.functions import udf
from matplotlib.font_manager import FontProperties

from config import *
from io_postgres import *
from aggregations import *
from visualization import *


'''
KPI 카드 (총 기사수, 고유 카테고리, TOP 키워드, 전일 대비 증감)

일자 트렌드(최근 14/30일) — dm_daily_summary에서 읽어서 라인차트

시간대 분포(0–23시) — 당일 write_date에서 hour 그룹집계, 바/히트맵

TOP 키워드 바 차트

워드클라우드
'''


def _parse_keywords(json_value):
    try:
        out = []
        for x in json.loads(json_value):
            if isinstance(x, str):
                s = x.strip().lower()
                if s:
                    out.append(s)
        return out
    except Exception:
        return []


def main():
    report_dt, yester_dt = dates_kst_now()
    report_date_str, yester_date_str, yester_start_ts, yester_end_ts, yester_title_str = date_strings(report_dt, yester_dt)
    report_path = f"{REPORT_DIR}/daily_report_{report_date_str}.pdf"

    # Font
    fp = FontProperties(fname=FONT_PATH, size=12)
    plt.rcParams["font.family"] = fp.get_name()
    plt.rcParams["axes.unicode_minus"] = False

    # Spark Session
    spark = (SparkSession.builder
        .appName("DailyNewsReport-Postgres")
        .master("spark://spark-master:7077")
        .getOrCreate()
    )

    df = load_news_article(spark, yester_start_ts, yester_end_ts)

    if df is None:
        logger.error("No data loaded for previous day.")
        return
    logger.info("Loaded yesterday rows: {}", df.count())
    

    parse_keywords_udf = udf(_parse_keywords, ArrayType(StringType()))
    dm_kw  = build_top_keywords_from_json(df, parse_keywords_udf, yester_date_str, top_n=10)
    dm_cat = build_category_counts_df(df, yester_date_str, top_n=10)
    dm_sum = build_summary_df(df, yester_date_str, spark)
    dm_hour = build_hourly_counts_df(spark, df, yester_date_str)

    # rows for charts
    kw_rows  = dm_kw.select("keyword", "count").orderBy("count", ascending=False).toPandas().to_dict("records")
    cat_rows = dm_cat.select("category", "count").orderBy("count", ascending=False).toPandas().to_dict("records")

    trend_df = load_trend_14d(spark, yester_date_str).toPandas()
    dod = compute_dod_from_trend_pdf(trend_df)
    sum_row = dm_sum.collect()[0].asDict()

    hour_pdf = dm_hour.toPandas()
    hours = list(range(24))
    h2c = {int(r["hour"]): int(r["count"]) for _, r in hour_pdf.iterrows()} if not hour_pdf.empty else {}
    hour_counts = [h2c.get(h, 0) for h in hours]

    
    figs = [
        plot_kpi(sum_row, kw_rows, dod, yester_title_str, fp),
        plot_trend(trend_df, sum_row, yester_date_str, fp),
        fig_hourly_bar(hours, hour_counts, yester_title_str, fp),
        plot_keyword_counts(kw_rows, yester_title_str, fp),
        plot_category_counts(cat_rows, yester_title_str, fp),
        plot_wordcloud(kw_rows, yester_title_str, FONT_PATH),
    ]
    save_pdf(report_path, figs)
    logger.info("Report saved: {}", report_path)

    save_df(dm_kw,  DM_KEYWORDS_TABLE, mode="append")
    save_df(dm_cat, DM_CATEGORY_TABLE, mode="append")
    save_df(dm_sum, DM_SUMMARY_TABLE,  mode="append")
    logger.info("Data Marts persisted. Done.")

if __name__ == "__main__":
    main()
