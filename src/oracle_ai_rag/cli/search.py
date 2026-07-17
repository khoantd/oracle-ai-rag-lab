"""Vector search smoke demo (lab sample questions)."""

from __future__ import annotations

import argparse
import sys

from oracle_ai_rag.config import load_settings
from oracle_ai_rag.db import get_connection
from oracle_ai_rag.embeddings import EmbeddingModel
from oracle_ai_rag.repository import OracleDocsRepository

SAMPLE_QUESTIONS = [
    "Why SQL has high buffer gets?",
    "How to fix ORA-01555 snapshot too old?",
    "Why Oracle chooses full table scan?",
    "Data Guard standby database has apply lag",
    "RMAN backup failed yesterday",
    "How to analyze AWR report?",
    "Oracle RAC gc buffer busy wait problem",
    "ORA-04031 shared pool memory error",
    "Find blocking session in Oracle database",
    "SQL execution plan changed after statistics gathering",
]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run sample (or custom) questions against pgvector search."
    )
    parser.add_argument(
        "question",
        nargs="*",
        help="Optional custom question(s). If omitted, runs the lab sample set.",
    )
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    settings = load_settings()
    questions = args.question if args.question else SAMPLE_QUESTIONS

    print("\nLoading embedding model...")
    embedder = EmbeddingModel(settings.embed_model)
    embedder.load()
    print("Model loaded")

    conn = get_connection(settings)
    try:
        repo = OracleDocsRepository(conn)
        for question in questions:
            print("\n")
            print("=" * 70)
            print("QUESTION:")
            print(question)
            print("-" * 70)

            vector = embedder.encode_text(question)
            results = repo.search(
                vector,
                top_k=settings.top_k,
                include_id=True,
            )

            for hit in results:
                snippet = hit.content[:200]
                print(
                    f"""
ID:
{hit.doc_id}

Title:
{hit.title}

Category:
{hit.category}

Similarity Distance:
{round(hit.distance, 4)}

Content:
{snippet}...

"""
                )
    finally:
        conn.close()

    return 0


def main() -> None:
    try:
        raise SystemExit(run())
    except ValueError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
