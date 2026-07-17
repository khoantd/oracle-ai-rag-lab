# Contributing to Oracle AI RAG Lab

Thanks for helping improve this learning lab. The goal is a clean, installable
Python package with a clear RAG pipeline that new contributors can run locally.

## Prerequisites

- Python 3.10+
- PostgreSQL 16 with [pgvector](https://github.com/pgvector/pgvector)
- [Ollama](https://ollama.com/) (for the chatbot step)
- Network on first run to download the SentenceTransformer model

## Setup

```bash
git clone <this-repo>
cd oracle-ai-rag-lab
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
cp .env.example .env
# Edit .env — set PGHOST, PGUSER, PGPASSWORD, etc. Never commit .env.
```

Apply the schema (once per database):

```bash
psql -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" -f sql/schema.sql
```

## Lab commands

```bash
oracle-rag-load                 # embed knowledge/ JSON → oracle_docs (--replace by default)
oracle-rag-search               # sample retrieval questions
oracle-rag-chat                 # interactive RAG chatbot
```

Use `--no-replace` on load if you must append without wiping existing rows.

## Adding knowledge

1. Add a JSON file under `knowledge/<category>/` with this shape:

```json
{
  "title": "Short problem title",
  "category": "Category Name",
  "content": "Problem / symptoms / diagnosis / solution prose"
}
```

2. Run `oracle-rag-load` so embeddings are refreshed.
3. Prefer clear DBA troubleshooting content over marketing copy.

## Tests and lint

```bash
ruff check src tests
pytest -m "not integration" -q
```

Integration smoke (needs a live DB and `PGHOST` set):

```bash
pytest -m integration -q
```

## Pull request checklist

- [ ] No secrets or `.env` files committed
- [ ] Unit tests pass (`pytest -m "not integration"`)
- [ ] `ruff check src tests` is clean
- [ ] New knowledge JSON validates (`title`, `category`, `content`)
- [ ] README / this guide updated if commands or layout changed

## Architecture notes

| Module | Role |
|--------|------|
| `config.Settings` | Env-based configuration |
| `repository.OracleDocsRepository` | SQL for insert / clear / vector search |
| `embeddings.EmbeddingModel` | SentenceTransformer wrapper |
| `rag.RagPipeline` | Retrieve → context → Ollama |
| `cli.*` | Thin argparse entry points only |

Keep business logic out of CLI modules. Prefer small, tested functions over large scripts.
