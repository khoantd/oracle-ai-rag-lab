"""Load and validate Oracle DBA knowledge JSON files."""

from __future__ import annotations

import json
from pathlib import Path

from oracle_ai_rag.models import Document


def load_documents(knowledge_dir: Path) -> list[Document]:
    """Scan knowledge_dir recursively for *.json and return validated documents."""
    if not knowledge_dir.is_dir():
        raise FileNotFoundError(f"Knowledge directory not found: {knowledge_dir}")

    documents: list[Document] = []
    for json_file in sorted(knowledge_dir.rglob("*.json")):
        with json_file.open(encoding="utf-8") as handle:
            data = json.load(handle)
        try:
            documents.append(Document.from_dict(data))
        except ValueError as exc:
            raise ValueError(f"{json_file}: {exc}") from exc
    return documents
