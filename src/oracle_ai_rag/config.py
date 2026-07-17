"""Application settings loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Repo root: src/oracle_ai_rag/config.py -> parents[2]
_REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    """Runtime configuration for DB, embeddings, and the LLM."""

    pg_host: str
    pg_port: int
    pg_database: str
    pg_user: str
    pg_password: str
    embed_model: str
    ollama_base_url: str
    ollama_model: str
    ollama_api_key: str
    top_k: int
    knowledge_dir: Path

    def require_db_password(self) -> None:
        if not self.pg_password:
            raise ValueError(
                "PGPASSWORD is not set. Copy .env.example to .env and set "
                "database credentials before connecting."
            )


def _env(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return value


def load_settings(*, env_file: Path | None = None) -> Settings:
    """Load settings from process env, optionally after reading a .env file."""
    if env_file is not None:
        load_dotenv(env_file)
    else:
        load_dotenv(_REPO_ROOT / ".env")
        load_dotenv()

    knowledge = _env("KNOWLEDGE_DIR")
    knowledge_dir = (
        Path(knowledge).expanduser().resolve()
        if knowledge
        else (_REPO_ROOT / "knowledge").resolve()
    )

    password = _env("PGPASSWORD", "") or ""

    return Settings(
        pg_host=_env("PGHOST", "localhost") or "localhost",
        pg_port=int(_env("PGPORT", "5432") or "5432"),
        pg_database=_env("PGDATABASE", "oracle_ai") or "oracle_ai",
        pg_user=_env("PGUSER", "ai_dba") or "ai_dba",
        pg_password=password,
        embed_model=(
            _env("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
            or "sentence-transformers/all-MiniLM-L6-v2"
        ),
        ollama_base_url=(
            _env("OLLAMA_BASE_URL", "http://localhost:11434/v1")
            or "http://localhost:11434/v1"
        ),
        ollama_model=_env("OLLAMA_MODEL", "qwen2.5:7b") or "qwen2.5:7b",
        ollama_api_key=_env("OLLAMA_API_KEY", "ollama") or "ollama",
        top_k=int(_env("TOP_K", "5") or "5"),
        knowledge_dir=knowledge_dir,
    )
