"""Load knowledge JSON into pgvector (oracle_docs)."""

from __future__ import annotations

import argparse
import sys
from dataclasses import replace
from pathlib import Path

from oracle_ai_rag.config import load_settings
from oracle_ai_rag.db import get_connection
from oracle_ai_rag.embeddings import EmbeddingModel
from oracle_ai_rag.knowledge import load_documents
from oracle_ai_rag.repository import OracleDocsRepository


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Embed Oracle DBA knowledge JSON and load into PostgreSQL pgvector."
    )
    parser.add_argument(
        "--replace",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Delete existing oracle_docs rows before insert (default: true).",
    )
    parser.add_argument(
        "--knowledge-dir",
        type=str,
        default=None,
        help="Override KNOWLEDGE_DIR / default knowledge/ path.",
    )
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    settings = load_settings()
    if args.knowledge_dir:
        settings = replace(
            settings,
            knowledge_dir=Path(args.knowledge_dir).expanduser().resolve(),
        )

    print("\nLoading embedding model...")
    embedder = EmbeddingModel(settings.embed_model)
    embedder.load()
    print("Embedding model loaded")

    print("\nConnecting PostgreSQL...")
    conn = get_connection(settings)
    repo = OracleDocsRepository(conn)
    print("PostgreSQL connected")

    if args.replace:
        print("\nCleaning old documents...")
        repo.clear()

    print("\nScanning knowledge folder...")
    documents = load_documents(settings.knowledge_dir)
    for doc in documents:
        print(f"Found: {doc.title}")
    print(f"\nTotal documents found: {len(documents)}")

    print("\nGenerating embeddings...\n")
    for index, document in enumerate(documents, start=1):
        embedding = embedder.encode_text(document.embedding_text())
        repo.insert(document, embedding)
        print(f"[{index}/{len(documents)}] Inserted: {document.title}")

    repo.commit()
    count = repo.count()
    conn.close()

    print("\n==============================")
    print("Documents in database:", count)
    print("==============================")
    print("\nLoad completed successfully!")
    return 0


def main() -> None:
    try:
        raise SystemExit(run())
    except ValueError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
