# Oracle AI DBA RAG Lab

## Build Oracle DBA Assistant using PostgreSQL pgvector + Ollama

---

# 1. Overview

This lab builds a local Oracle DBA AI Assistant using Retrieval Augmented Generation (RAG).

The system combines:

- Oracle DBA Knowledge Base (JSON documents)
- Sentence Transformer Embedding Model
- PostgreSQL 16 + pgvector
- HNSW Vector Search
- Ollama Local LLM

The goal is to allow an AI assistant to answer Oracle Database troubleshooting questions based on DBA knowledge.

---

# 2. Architecture

```text
            Oracle DBA Knowledge
                   |
             JSON Documents
                   |
                   v
    Sentence Transformer Embedding
         all-MiniLM-L6-v2
                   |
          Vector Dimension: 384
                   |
                   v
         PostgreSQL 16 + pgvector
            oracle_docs table
                   |
          HNSW Similarity Search
                   |
                   v
             RAG Application
                   |
                   v
          Ollama Local LLM
         Qwen2.5 / Qwen3
                   |
                   v
          Oracle DBA Assistant
```

# 3. Lab Objectives

## Vector Database

- What is embedding
- How text becomes vector representation
- How pgvector stores embeddings
- How similarity search works

## RAG Pipeline

- Retrieve relevant documents
- Build context
- Send context to LLM
- Generate DBA response

## AI DBA Architecture

- Oracle Performance Advisor
- SQL Tuning Assistant
- AWR Analyzer
- Incident Diagnosis Agent
- Autonomous DBA Agent

# 4. Technology Stack

| Component | Technology |
|---|---|
| Database | PostgreSQL 16 |
| Vector Extension | pgvector 0.8.5 |
| Embedding Model | all-MiniLM-L6-v2 |
| LLM | Ollama Qwen2.5/Qwen3 |
| Language | Python 3 |
| Framework | Custom RAG Pipeline |

# 5. Environment Architecture

```text
Windows Host
+-----------------------------+
| Python RAG Application      |
| Ollama Qwen Model           |
+-------------+---------------+
              |
           Network
              |
Oracle Linux VM
+-----------------------------+
| PostgreSQL 16              |
| pgvector                   |
| oracle_ai database         |
+----------------------------+
```

# 6. Project Structure

```text
oracle-ai-rag-lab/
├── knowledge/
├── python/
│   ├── db.py
│   ├── 01_load_oracle_dba_knowledge.py
│   ├── 02_vector_search_test.py
│   └── 03_rag_chatbot.py
├── requirements.txt
└── README.md
```

# 7. Knowledge Base

- SQL Performance (15)
- Execution Plans (10)
- Oracle Errors (10)
- Database Administration (10)
- Monitoring (5)

# 8. Database Setup

```sql
CREATE DATABASE oracle_ai;
```

```sql
CREATE EXTENSION vector;
```

# 9. Create Vector Table

```sql
CREATE TABLE oracle_docs (
    id SERIAL PRIMARY KEY,
    title TEXT,
    category TEXT,
    content TEXT,
    embedding VECTOR(384)
);
```

# 10. Create HNSW Index

```sql
CREATE INDEX oracle_docs_embedding_hnsw
ON oracle_docs
USING hnsw (embedding vector_cosine_ops);
```

# 11. Python Environment

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

requirements.txt

```text
sentence-transformers
psycopg2-binary
numpy
openai
```

# 12. Load Knowledge

```bash
cd python
python 01_load_oracle_dba_knowledge.py
```

# 13. Test Vector Search

```bash
python 02_vector_search_test.py
```

# 14. Start Ollama

```bash
ollama list
ollama pull qwen2.5:7b
ollama serve
```

# 15. Run RAG Chatbot

```bash
python 03_rag_chatbot.py
```

# 16. RAG Flow Explanation

1. Create question embedding.
2. Search similar vectors in pgvector.
3. Build context from retrieved documents.
4. Send context and question to the LLM.
5. Generate the Oracle DBA answer.
