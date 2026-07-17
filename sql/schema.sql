-- Oracle AI RAG Lab: PostgreSQL + pgvector schema
-- Run against database oracle_ai after: CREATE DATABASE oracle_ai;

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS oracle_docs (
    id SERIAL PRIMARY KEY,
    title TEXT,
    category TEXT,
    content TEXT,
    embedding VECTOR(384)
);

CREATE INDEX IF NOT EXISTS oracle_docs_embedding_hnsw
ON oracle_docs
USING hnsw (embedding vector_cosine_ops);
