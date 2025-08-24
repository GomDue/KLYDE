CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS news_article (
    id SERIAL PRIMARY KEY,
    title      TEXT NOT NULL,
    writer     VARCHAR(255) NOT NULL,
    write_date TIMESTAMP NOT NULL,
    category   VARCHAR(50) NOT NULL,
    content    TEXT NOT NULL,
    url        TEXT UNIQUE NOT NULL,
    keywords   JSONB DEFAULT '[]'::jsonb,
    embedding  VECTOR(1536) NULL,
    read       INTEGER DEFAULT 0,
    updated    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_news_article_write_date ON news_article(write_date);
CREATE INDEX IF NOT EXISTS idx_news_article_category   ON news_article(category);

-- DM: 일일 키워드 TOP N
CREATE TABLE IF NOT EXISTS dm_daily_top_keywords (
  report_date DATE NOT NULL,
  rank        INT  NOT NULL,
  keyword     TEXT NOT NULL,
  count       INT  NOT NULL,
  PRIMARY KEY (report_date, rank)
);
CREATE INDEX IF NOT EXISTS idx_dm_kw_date ON dm_daily_top_keywords(report_date);

-- DM: 일일 카테고리 기사 수 TOP N
CREATE TABLE IF NOT EXISTS dm_daily_category_counts (
  report_date DATE NOT NULL,
  rank        INT  NOT NULL,
  category    TEXT NOT NULL,
  count       INT  NOT NULL,
  PRIMARY KEY (report_date, rank)
);
CREATE INDEX IF NOT EXISTS idx_dm_cat_date ON dm_daily_category_counts(report_date);

-- DM: 일일 요약
CREATE TABLE IF NOT EXISTS dm_daily_summary (
  report_date     DATE PRIMARY KEY,
  total_articles  INT  NOT NULL,
  unique_categories INT NOT NULL
);
