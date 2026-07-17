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

# 16. Release Notes

## 0.1.0 — Open-source package refactor

First packaged release of the Oracle DBA RAG lab. The numbered `python/` scripts are replaced by an installable library and CLIs; the step-by-step lab flow is unchanged.

### Why these changes

The original layout was a tutorial of standalone scripts: credentials lived in source, vector-search SQL was copied between files, and there was no installable package, automated tests, or contributor guide. That works for a private lab, but it blocks safe sharing and makes pull requests hard to review.

This release reorganizes the same RAG learning path into a small library with thin CLIs so the lab stays teachable while meeting common open-source expectations (config via env, one place for SQL, tests, license, contributing docs).

### Benefits

| Change | Benefit |
|--------|---------|
| Installable `oracle-ai-rag` package | Contributors run `pip install -e .` from any directory; no CWD/`PYTHONPATH` hacks |
| Shared repository + RAG modules | One vector-search path for search and chat — fewer bugs when you improve retrieval |
| Env-based Settings (`.env.example`) | Secrets stay out of git; each machine/VM can use its own DB without editing code |
| Explicit `--replace` / `--no-replace` on load | Destructive wipe is visible and documented; safer for shared databases |
| `sql/schema.sql` in-repo | Newcomers can create the pgvector schema without scavenging SQL from README alone |
| Tests + ruff + CI | Changes can be verified offline before touching a live Postgres/Ollama stack |
| MIT + `CONTRIBUTING.md` | Clear license and PR checklist so forks and contributions have a known contract |
| Thin CLI adapters | Lab steps stay simple (`oracle-rag-load` …) while logic lives in testable modules |

### Added

- Installable package `oracle-ai-rag` (`src/oracle_ai_rag/`) via `pip install -e .`
- Console commands: `oracle-rag-load`, `oracle-rag-search`, `oracle-rag-chat`
- Env-based configuration (`.env.example`) — no database secrets in source
- Shared modules: Settings, repository (vector search SQL), embeddings, RAG pipeline, knowledge loader
- `sql/schema.sql` for pgvector table + HNSW index
- Unit tests (`pytest`), lint (`ruff`), and GitHub Actions CI
- MIT `LICENSE` and `CONTRIBUTING.md`

### Changed

- Project layout moved from flat lab scripts to `src/` package + thin CLI adapters
- README lab steps now use the new CLI entry points
- Load wipe behavior is explicit (`oracle-rag-load --replace` by default; `--no-replace` to skip)

### Removed

- Legacy `python/` scripts (`01_load_…`, `02_vector_search_…`, `03_rag_chatbot`, `db.py`, smoke scripts)
- Hardcoded PostgreSQL host/user/password from source

### Migration (from pre-0.1.0 scripts)

```bash
pip install -e .
cp .env.example .env   # set PGHOST, PGUSER, PGPASSWORD, etc.

# Old                              New
# python 01_load_….py           →  oracle-rag-load
# python 02_vector_search_….py  →  oracle-rag-search
# python 03_rag_chatbot.py      →  oracle-rag-chat
```

# 17. License

MIT — see [LICENSE](LICENSE).
