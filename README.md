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
| Vector Extension | pgvector |
| Embedding Model | all-MiniLM-L6-v2 |
| LLM | Ollama Qwen2.5/Qwen3 |
| Language | Python 3.10+ |
| Packaging | `oracle-ai-rag` (`pip install -e .`) |

# 5. Environment Architecture

```text
Developer Machine
+-----------------------------+
| Python RAG package (CLI)    |
| Ollama Qwen Model           |
+-------------+---------------+
              |
           Network
              |
PostgreSQL host
+-----------------------------+
| PostgreSQL 16               |
| pgvector                    |
| oracle_ai database          |
+-----------------------------+
```

# 6. Project Structure

```text
oracle-ai-rag-lab/
├── knowledge/                 # Oracle DBA JSON knowledge base
├── src/oracle_ai_rag/         # Installable package
│   ├── config.py
│   ├── db.py
│   ├── embeddings.py
│   ├── knowledge.py
│   ├── repository.py
│   ├── rag.py
│   └── cli/                   # load / search / chat
├── sql/schema.sql             # pgvector table + HNSW index
├── tests/
├── pyproject.toml
├── .env.example
├── CONTRIBUTING.md
└── README.md
```

# 7. Knowledge Base

- SQL Performance (15)
- Execution Plans (10)
- Oracle Errors (10)
- Database Administration (10)
- Monitoring (5)

# 8. Quick start for contributors

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# Edit .env with your PostgreSQL credentials (never commit .env)
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for PR guidelines and tests.

# 9. Database Setup

```sql
CREATE DATABASE oracle_ai;
```

Then apply the checked-in schema:

```bash
psql -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" -f sql/schema.sql
```

Or run the SQL manually:

```sql
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
```

# 10. Python Environment

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
pip install -e .
cp .env.example .env
```

Required env vars (see `.env.example`): `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`.

# 11. Load Knowledge

```bash
oracle-rag-load
```

By default this **replaces** all rows in `oracle_docs`. Use `oracle-rag-load --no-replace` to skip the wipe.

# 12. Test Vector Search

```bash
oracle-rag-search
```

# 13. Start Ollama

```bash
ollama list
ollama pull qwen2.5:7b
ollama serve
```

# 14. Run RAG Chatbot

```bash
oracle-rag-chat
```

# 15. RAG Flow Explanation

1. Create question embedding.
2. Search similar vectors in pgvector.
3. Build context from retrieved documents.
4. Send context and question to the LLM.
5. Generate the Oracle DBA answer.

# 16. License

MIT — see [LICENSE](LICENSE).
