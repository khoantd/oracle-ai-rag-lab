"""Interactive Oracle DBA RAG chatbot."""

from __future__ import annotations

import argparse
import sys

from oracle_ai_rag.config import load_settings
from oracle_ai_rag.rag import RagPipeline


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Interactive RAG chatbot backed by pgvector + Ollama."
    )
    parser.add_argument(
        "--once",
        type=str,
        default=None,
        help="Ask a single question and exit (useful for scripts/tests).",
    )
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    settings = load_settings()
    pipeline = RagPipeline(settings)

    print("Loading embedding model...")
    pipeline.embedding_model.load()
    print("Embedding model ready")

    if args.once is not None:
        answer = pipeline.answer(args.once)
        print("\n========== AI DBA ==========")
        print(answer)
        print("============================")
        return 0

    print("\nOracle AI DBA RAG Chatbot")
    print("Type exit to stop\n")

    while True:
        question = input("\nDBA Question: ")
        if question.strip().lower() == "exit":
            break
        if not question.strip():
            continue

        answer = pipeline.answer(question)
        print("\n========== AI DBA ==========")
        print(answer)
        print("============================")

    return 0


def main() -> None:
    try:
        raise SystemExit(run())
    except ValueError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        raise SystemExit(130) from None


if __name__ == "__main__":
    main()
