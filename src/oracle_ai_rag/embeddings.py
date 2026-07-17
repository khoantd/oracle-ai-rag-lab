"""Sentence-transformer embedding wrapper."""

from __future__ import annotations

from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """Lazy-friendly wrapper around SentenceTransformer."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model: SentenceTransformer | None = None

    def load(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def encode_text(self, text: str) -> list[float]:
        model = self.load()
        return model.encode(text).tolist()
