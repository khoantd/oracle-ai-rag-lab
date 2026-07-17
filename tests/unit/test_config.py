"""Unit tests for Settings / env loading."""

from __future__ import annotations

import pytest

from oracle_ai_rag.config import Settings, load_settings


def test_load_settings_from_env(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setenv("PGHOST", "db.example")
    monkeypatch.setenv("PGPORT", "5433")
    monkeypatch.setenv("PGDATABASE", "testdb")
    monkeypatch.setenv("PGUSER", "tester")
    monkeypatch.setenv("PGPASSWORD", "secret")
    monkeypatch.setenv("EMBED_MODEL", "custom-model")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
    monkeypatch.setenv("OLLAMA_MODEL", "llama3")
    monkeypatch.setenv("TOP_K", "3")
    monkeypatch.setenv("KNOWLEDGE_DIR", str(tmp_path))

    settings = load_settings(env_file=tmp_path / "missing.env")

    assert settings.pg_host == "db.example"
    assert settings.pg_port == 5433
    assert settings.pg_database == "testdb"
    assert settings.pg_user == "tester"
    assert settings.pg_password == "secret"
    assert settings.embed_model == "custom-model"
    assert settings.ollama_model == "llama3"
    assert settings.top_k == 3
    assert settings.knowledge_dir == tmp_path.resolve()


def test_require_db_password_raises_when_empty() -> None:
    settings = Settings(
        pg_host="localhost",
        pg_port=5432,
        pg_database="oracle_ai",
        pg_user="ai_dba",
        pg_password="",
        embed_model="m",
        ollama_base_url="http://localhost:11434/v1",
        ollama_model="qwen",
        ollama_api_key="ollama",
        top_k=5,
        knowledge_dir=__import__("pathlib").Path("."),
    )
    with pytest.raises(ValueError, match="PGPASSWORD"):
        settings.require_db_password()
