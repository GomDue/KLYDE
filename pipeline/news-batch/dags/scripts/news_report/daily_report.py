import json
import logging

from pyspark.sql import SparkSession
from pyspark.sql.types import ArrayType, StringType
from pyspark.sql.functions import udf
from matplotlib.font_manager import FontProperties

from config import *
from io_postgres import *
from aggregations import *
from visualization import *

log = logging.getLogger("daily-report")


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
    report_date_str, yester_date_str, yester_start_ts, yester_end_ts = date_strings(report_dt, yester_dt)
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
        log.error("No data loaded for previous day.")
        return
    log.info("Loaded yesterday rows: {}", df.count())
    

    parse_keywords_udf = udf(_parse_keywords, ArrayType(StringType()))
    dm_kw  = build_top_keywords_from_json(df, parse_keywords_udf, yester_date_str, top_n=10)
    dm_cat = build_category_counts_df(df, yester_date_str, top_n=10)
    dm_sum = build_summary_df(df, yester_date_str, spark)
    dm_hour = build_hourly_counts_df(spark, df, yester_date_str)

    # Rows for charts
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
        plot_kpi(sum_row, kw_rows, dod, report_date_str, fp),
        plot_trend(trend_df, sum_row, yester_date_str, fp),
        plot_hourly_bar(hours, hour_counts, report_date_str, fp),
        plot_keyword_counts(kw_rows, report_date_str, fp),
        plot_category_counts(cat_rows, report_date_str, fp),
        plot_wordcloud(kw_rows, report_date_str, FONT_PATH),
    ]
    save_pdf(report_path, figs)
    log.info("Report saved: {}", report_path)

    save_df(dm_kw,  DM_KEYWORDS_TABLE, mode="append")
    save_df(dm_cat, DM_CATEGORY_TABLE, mode="append")
    save_df(dm_sum, DM_SUMMARY_TABLE,  mode="append")
    log.info("Data Marts persisted. Done.")

if __name__ == "__main__":
    main()
