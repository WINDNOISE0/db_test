CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE knowledge_base (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(384)
);