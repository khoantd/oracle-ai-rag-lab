"""Unit tests for RAG context building."""

from __future__ import annotations

from oracle_ai_rag.models import SearchHit
from oracle_ai_rag.prompts import build_context, build_user_prompt


def test_build_context_includes_hits() -> None:
    hits = [
        SearchHit(
            title="High Buffer Gets",
            category="SQL Performance",
            content="Check indexes",
            distance=0.1,
        )
    ]
    context = build_context(hits)
    assert "High Buffer Gets" in context
    assert "SQL Performance" in context
    assert "Check indexes" in context


def test_build_user_prompt_includes_question_and_context() -> None:
    prompt = build_user_prompt("Why slow?", "CTX")
    assert "Why slow?" in prompt
    assert "CTX" in prompt
    assert "Root cause" in prompt
