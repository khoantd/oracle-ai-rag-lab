"""Persistence and vector search for oracle_docs."""

from __future__ import annotations

from collections.abc import Sequence

from psycopg2.extensions import connection as PgConnection

from oracle_ai_rag.models import Document, SearchHit


class OracleDocsRepository:
    """Repository for clearing, inserting, counting, and searching oracle_docs."""

    def __init__(self, conn: PgConnection) -> None:
        self._conn = conn

    def clear(self) -> None:
        with self._conn.cursor() as cursor:
            cursor.execute("DELETE FROM oracle_docs;")
        self._conn.commit()

    def insert(self, document: Document, embedding: Sequence[float]) -> None:
        with self._conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO oracle_docs (title, category, content, embedding)
                VALUES (%s, %s, %s, %s)
                """,
                (document.title, document.category, document.content, list(embedding)),
            )

    def commit(self) -> None:
        self._conn.commit()

    def count(self) -> int:
        with self._conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM oracle_docs;")
            row = cursor.fetchone()
        return int(row[0]) if row else 0

    def search(
        self,
        query_embedding: Sequence[float],
        *,
        top_k: int = 5,
        include_id: bool = False,
    ) -> list[SearchHit]:
        if include_id:
            sql = """
                SELECT id, title, category, content,
                       embedding <=> %s::vector AS distance
                FROM oracle_docs
                ORDER BY distance
                LIMIT %s
            """
        else:
            sql = """
                SELECT title, category, content,
                       embedding <=> %s::vector AS distance
                FROM oracle_docs
                ORDER BY distance
                LIMIT %s
            """

        with self._conn.cursor() as cursor:
            cursor.execute(sql, (list(query_embedding), top_k))
            rows = cursor.fetchall()

        hits: list[SearchHit] = []
        for row in rows:
            if include_id:
                hits.append(
                    SearchHit(
                        doc_id=int(row[0]),
                        title=row[1],
                        category=row[2],
                        content=row[3],
                        distance=float(row[4]),
                    )
                )
            else:
                hits.append(
                    SearchHit(
                        title=row[0],
                        category=row[1],
                        content=row[2],
                        distance=float(row[3]),
                    )
                )
        return hits
