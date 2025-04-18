CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    title TEXT,
    author TEXT,
    content TEXT,
    category TEXT,
    keywords TEXT[],
    embedding_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
