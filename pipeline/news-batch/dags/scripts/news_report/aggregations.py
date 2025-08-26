from pyspark.sql.functions import explode, desc, row_number, lit, col, to_date, hour, coalesce
from pyspark.sql.window import Window
from pyspark.sql.types import IntegerType


def build_top_keywords_from_json(df, parse_udf, yester_date_str, top_n=10):
    with_kw = df.withColumn("kw_arr", parse_udf(col("keywords")))
    exploded = with_kw.select(explode(col("kw_arr")).alias("keyword"))
    counts = exploded.groupBy("keyword").count().orderBy(desc("count")).limit(top_n)
    w = Window.orderBy(desc("count"))
    
    ranked = counts.withColumn("rank", row_number().over(w))
    ranked   = ranked.withColumn("report_date", to_date(lit(yester_date_str), "yyyy-MM-dd"))
    
    return ranked.select(
        "report_date",
        ranked["rank"].cast(IntegerType()).alias("rank"),
        "keyword",
        ranked["count"].cast(IntegerType()).alias("count"),
    )

def build_category_counts_df(df, yester_date_str, top_n=10):
    counts = df.groupBy("category").count().orderBy(desc("count")).limit(top_n)
    w = Window.orderBy(desc("count"))

    ranked = counts.withColumn("rank", row_number().over(w))
    ranked   = ranked.withColumn("report_date", to_date(lit(yester_date_str), "yyyy-MM-dd"))

    return ranked.select(
        "report_date",
        ranked["rank"].cast(IntegerType()).alias("rank"),
        "category",
        ranked["count"].cast(IntegerType()).alias("count"),
    )

def build_summary_df(df, yester_date_str, spark):
    total_articles = df.count()
    unique_categories = df.select("category").distinct().count()

    df = spark.createDataFrame(
        [(yester_date_str, int(total_articles), int(unique_categories))],
        ["report_date", "total_articles", "unique_categories"]
    )

    return (df
        .withColumn("report_date", to_date(col("report_date"), "yyyy-MM-dd"))
        .withColumn("total_articles", col("total_articles").cast(IntegerType()))
        .withColumn("unique_categories", col("unique_categories").cast(IntegerType()))
    )

def build_hourly_counts_df(spark, df, yester_date_str):
    counted = (
        df.select(hour(col("write_date")).alias("hour"))
          .groupBy("hour").count()
    )
    hours_df = spark.createDataFrame([(i,) for i in range(24)], "hour INT")
    filled = (
        hours_df.join(counted, on="hour", how="left")
                .withColumn("count", coalesce(col("count"), lit(0)))
    )
    return (
        filled.withColumn("report_date", to_date(lit(yester_date_str), "yyyy-MM-dd"))
              .select(
                  "report_date",
                  col("hour").cast(IntegerType()).alias("hour"),
                  col("count").cast(IntegerType()).alias("count"),
              )
              .orderBy("hour")
    )

def compute_dod_from_trend_pdf(trend_pdf):
    if trend_pdf is None or len(trend_pdf) < 2:
        return None
    prev = int(trend_pdf["total_articles"].iloc[-2])
    curr = int(trend_pdf["total_articles"].iloc[-1])
    if prev <= 0:
        return None
    return round((curr - prev) * 100.0 / prev, 1)

