# Project structure map

> Persistent overview for AI agents. Generated on first run by `/understand` (see `.cursor/commands/understand-project.md`). Update when architecture changes significantly.

## Meta

| Field | Value |
|-------|-------|
| **Updated** | 2026-07-17 |
| **Tool** | cursor |

## Stack

- **Language:** Python 3.10+
- **Package:** `oracle-ai-rag` (`src/oracle_ai_rag/`, `pyproject.toml`)
- **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`, 384-dim)
- **Vector DB:** PostgreSQL 16 + pgvector (HNSW cosine, table `oracle_docs`)
- **LLM:** Ollama via OpenAI-compatible client (`qwen2.5:7b` at `localhost:11434`)
- **Deps:** declared in `pyproject.toml` (+ `python-dotenv`); `requirements.txt` is `-e .`

## Layout

| Path | Purpose |
|------|---------|
| `src/oracle_ai_rag/` | Installable RAG library + CLIs |
| `src/oracle_ai_rag/cli/` | `load`, `search`, `chat` entry points |
| `sql/schema.sql` | Extension, `oracle_docs`, HNSW index |
| `knowledge/` | Oracle DBA JSON knowledge base (~50 docs across 5 categories) |
| `tests/unit/` | Offline unit tests |
| `tests/integration/` | Optional live-DB smoke (`@pytest.mark.integration`) |
| `.env.example` | Required env template (no secrets in source) |
| `CONTRIBUTING.md` / `LICENSE` | OSS contributor surface |
| `.github/workflows/ci.yml` | Ruff + unit tests |
| `tasks/` | Agent task checklist |
| `.agent/` | Session continuity + this project map |

## Entry points

- `oracle-rag-load` — scan `knowledge/**/*.json`, embed, insert into `oracle_docs`
- `oracle-rag-search` — cosine similarity search demo
- `oracle-rag-chat` — interactive RAG loop (retrieve → context → Ollama)

## Key files

- `src/oracle_ai_rag/config.py` — `Settings` from env
- `src/oracle_ai_rag/repository.py` — SQL clear/insert/search
- `src/oracle_ai_rag/rag.py` — `RagPipeline`
- `src/oracle_ai_rag/prompts.py` — context + user prompt builders
- `knowledge/**/*.json` — docs shaped as `{title, category, content}`

## Commands

| Action | Command |
|--------|---------|
| Install | `python -m venv .venv` then `pip install -e ".[dev]"` |
| Configure | `cp .env.example .env` (edit credentials) |
| Schema | `psql ... -f sql/schema.sql` |
| Load knowledge | `oracle-rag-load` |
| Test search | `oracle-rag-search` |
| Pull LLM | `ollama pull qwen2.5:7b` then `ollama serve` |
| Run chatbot | `oracle-rag-chat` |
| Unit tests | `pytest -m "not integration" -q` |
| Lint | `ruff check src tests` |

## Code intelligence

| Item | Status |
|------|--------|
| CodeGraph index | Present — `.codegraph/` |
| Workspace root | `/Volumes/Data/Software Development/Python/oracle-ai-rag-lab` |
| OntoSight | Optional — `npx royalsolution-ontosight@0.2.1 "<workspace-root>" --path src` |

## Notes

- Secrets must live in `.env` only; rotate any password previously hardcoded in old `python/db.py`.
- Knowledge JSON schema: `title`, `category`, `content`.
- Load defaults to `--replace` (wipe then reload); use `--no-replace` to skip wipe.
