"""RAG pipeline: retrieve context and ask the local LLM."""

from __future__ import annotations

from openai import OpenAI

from oracle_ai_rag.config import Settings
from oracle_ai_rag.db import get_connection
from oracle_ai_rag.embeddings import EmbeddingModel
from oracle_ai_rag.models import SearchHit
from oracle_ai_rag.prompts import SYSTEM_PROMPT, build_context, build_user_prompt
from oracle_ai_rag.repository import OracleDocsRepository

__all__ = [
    "RagPipeline",
    "SYSTEM_PROMPT",
    "build_context",
    "build_user_prompt",
]


class RagPipeline:
    """Compose embedding search + Ollama chat completion."""

    def __init__(
        self,
        settings: Settings,
        embedding_model: EmbeddingModel | None = None,
        client: OpenAI | None = None,
    ) -> None:
        self.settings = settings
        self.embedding_model = embedding_model or EmbeddingModel(settings.embed_model)
        self.client = client or OpenAI(
            base_url=settings.ollama_base_url,
            api_key=settings.ollama_api_key,
        )

    def retrieve(self, question: str) -> list[SearchHit]:
        vector = self.embedding_model.encode_text(question)
        conn = get_connection(self.settings)
        try:
            repo = OracleDocsRepository(conn)
            return repo.search(vector, top_k=self.settings.top_k, include_id=False)
        finally:
            conn.close()

    def ask_llm(self, question: str, context: str) -> str:
        response = self.client.chat.completions.create(
            model=self.settings.ollama_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": build_user_prompt(question, context),
                },
            ],
            temperature=0.2,
        )
        content = response.choices[0].message.content
        return content or ""

    def answer(self, question: str) -> str:
        hits = self.retrieve(question)
        context = build_context(hits)
        return self.ask_llm(question, context)
