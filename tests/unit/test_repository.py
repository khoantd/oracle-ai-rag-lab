"""Unit tests for OracleDocsRepository with a mocked connection."""

from __future__ import annotations

from unittest.mock import MagicMock

from oracle_ai_rag.models import Document
from oracle_ai_rag.repository import OracleDocsRepository


def test_clear_executes_delete() -> None:
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value.__enter__.return_value = cursor

    repo = OracleDocsRepository(conn)
    repo.clear()

    cursor.execute.assert_called_once_with("DELETE FROM oracle_docs;")
    conn.commit.assert_called_once()


def test_insert_passes_document_and_embedding() -> None:
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value.__enter__.return_value = cursor

    repo = OracleDocsRepository(conn)
    doc = Document(title="T", category="C", content="Body")
    repo.insert(doc, [0.1, 0.2, 0.3])

    args = cursor.execute.call_args
    assert "INSERT INTO oracle_docs" in args[0][0]
    assert args[0][1] == ("T", "C", "Body", [0.1, 0.2, 0.3])


def test_search_maps_rows_with_id() -> None:
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value.__enter__.return_value = cursor
    cursor.fetchall.return_value = [
        (7, "Title", "Cat", "Content", 0.42),
    ]

    repo = OracleDocsRepository(conn)
    hits = repo.search([0.0] * 3, top_k=5, include_id=True)

    assert len(hits) == 1
    assert hits[0].doc_id == 7
    assert hits[0].title == "Title"
    assert hits[0].distance == 0.42
    sql = cursor.execute.call_args[0][0]
    assert "<=>" in sql
    assert cursor.execute.call_args[0][1] == ([0.0, 0.0, 0.0], 5)


def test_count_returns_integer() -> None:
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value.__enter__.return_value = cursor
    cursor.fetchone.return_value = (12,)

    repo = OracleDocsRepository(conn)
    assert repo.count() == 12
