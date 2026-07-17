# Agent session

> Cross-tool handoff state for Cursor, Claude Code, and Kiro. Update at session end (`/handoff`) or phase changes; read at session start (`/resume`).

## Meta

| Field | Value |
|-------|-------|
| **Updated** | 2026-07-17 |
| **Phase** | build |
| **Tool** | cursor |
| **Persona** | backend |

## Goal

Refactor the Oracle DBA RAG lab into an installable open-source Python package with thin CLIs, env-based config, tests, and contributor docs—while keeping the learning-lab README narrative.

## Done

- `src/oracle_ai_rag/` package with Settings, repository, embeddings, RAG, prompts
- Console scripts: `oracle-rag-load`, `oracle-rag-search`, `oracle-rag-chat`
- `sql/schema.sql`, `.env.example`, `pyproject.toml`, MIT LICENSE, CONTRIBUTING, README
- Unit tests + CI workflow; removed legacy `python/` scripts with hardcoded secrets

## In progress

- _(none)_
- **Blockers:** none

## Next

1. Run `pip install -e ".[dev]"` and `pytest -m "not integration"` locally to confirm
2. Copy `.env.example` → `.env` with real DB credentials and smoke-test CLIs against pgvector
3. Rotate any password that was previously committed in `python/db.py` if the DB is still reachable

## Decisions

- MIT license; src layout; wipe-on-load behind `--replace` (default true)
- CI installs light deps only (no sentence-transformers) for unit tests

## Gotchas

- First full install still downloads the embedding model; chatbot needs Ollama running
- Do not commit `.env`

## Pointers

| Item | Location |
|------|----------|
| Spec | plan: OSS Package Refactor |
| Tasks | `tasks/todo.md` |
| Branch | _(local)_ |
| Key files | `src/oracle_ai_rag/`, `pyproject.toml`, `CONTRIBUTING.md` |
