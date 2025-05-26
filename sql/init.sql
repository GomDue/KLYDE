-- Connect to the 'news' database
\c news;

-- Create necessary extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the 'news_article' table
CREATE TABLE IF NOT EXISTS news_article (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    writer VARCHAR(255) NOT NULL,
    write_date TIMESTAMP NOT NULL,
    category VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    keywords JSON DEFAULT '[]'::json,
    embedding VECTOR(1536) NULL,
    read INTEGER DEFAULT 0
);

-- Grant privileges on the 'news_article' table to ssafy user
GRANT ALL PRIVILEGES ON TABLE news_article TO ssafy;
