"""Domain models for knowledge documents and search results."""

from __future__ import annotations

from dataclasses import dataclass

REQUIRED_DOC_KEYS = ("title", "category", "content")


@dataclass(frozen=True)
class Document:
    title: str
    category: str
    content: str

    @classmethod
    def from_dict(cls, data: dict) -> Document:
        missing = [key for key in REQUIRED_DOC_KEYS if key not in data]
        if missing:
            raise ValueError(f"Document missing required keys: {missing}")
        return cls(
            title=str(data["title"]),
            category=str(data["category"]),
            content=str(data["content"]),
        )

    def embedding_text(self) -> str:
        return (
            f"Title:\n{self.title}\n\n"
            f"Category:\n{self.category}\n\n"
            f"Content:\n{self.content}\n"
        )


@dataclass(frozen=True)
class SearchHit:
    title: str
    category: str
    content: str
    distance: float
    doc_id: int | None = None
