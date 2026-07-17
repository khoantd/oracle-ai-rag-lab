"""Prompt and context formatting for the RAG chatbot."""

from __future__ import annotations

from oracle_ai_rag.models import SearchHit

SYSTEM_PROMPT = "You are an Oracle DBA expert."


def build_context(hits: list[SearchHit]) -> str:
    """Format retrieved hits into a prompt context block."""
    parts: list[str] = []
    for hit in hits:
        parts.append(
            f"Title:\n{hit.title}\n\n"
            f"Category:\n{hit.category}\n\n"
            f"Knowledge:\n{hit.content}\n\n"
            "----------------------\n"
        )
    return "\n".join(parts)


def build_user_prompt(question: str, context: str) -> str:
    return f"""
You are an Oracle Database Expert AI Assistant.

Answer the question using ONLY the provided Oracle DBA knowledge.

If the knowledge does not contain the answer,
say:

"I don't have enough Oracle knowledge."

=====================
Oracle DBA Knowledge
=====================

{context}

=====================
Question
=====================

{question}

Provide:

1. Root cause

2. Diagnosis steps

3. Recommended solution
"""
