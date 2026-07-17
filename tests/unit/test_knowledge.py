"""Unit tests for Document / knowledge loading."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from oracle_ai_rag.knowledge import load_documents
from oracle_ai_rag.models import Document


def test_document_from_dict_and_embedding_text() -> None:
    doc = Document.from_dict(
        {"title": "T", "category": "C", "content": "Body"}
    )
    assert doc.title == "T"
    text = doc.embedding_text()
    assert "Title:\nT" in text
    assert "Category:\nC" in text
    assert "Content:\nBody" in text


def test_document_missing_keys() -> None:
    with pytest.raises(ValueError, match="missing required keys"):
        Document.from_dict({"title": "only"})


def test_load_documents_from_tree(tmp_path: Path) -> None:
    sub = tmp_path / "sql_performance"
    sub.mkdir()
    payload = {"title": "Missing Index", "category": "SQL", "content": "Add index"}
    (sub / "01.json").write_text(json.dumps(payload), encoding="utf-8")

    docs = load_documents(tmp_path)
    assert len(docs) == 1
    assert docs[0].title == "Missing Index"


def test_load_documents_rejects_invalid_json_shape(tmp_path: Path) -> None:
    (tmp_path / "bad.json").write_text(json.dumps({"title": "x"}), encoding="utf-8")
    with pytest.raises(ValueError, match="missing required keys"):
        load_documents(tmp_path)


def test_load_documents_missing_dir(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_documents(tmp_path / "nope")
