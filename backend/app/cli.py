import argparse
import sys
from pathlib import Path

from .config import get_settings
from .embeddings import get_embedder
from .ingestion.pipeline import ingest_file
from .llm import get_llm_client
from .retrieval.pipeline import answer_question
from .vectorstore import get_vector_store


def ingest(args: argparse.Namespace) -> None:
    settings = get_settings()
    embedder = get_embedder(settings)
    store = get_vector_store(settings)

    chunks = ingest_file(Path(args.path), settings, embedder, store)
    print(f"ingested {len(chunks)} chunks from {args.path}")
    for c in chunks[:3]:
        preview = c.text[:80].replace("\n", " ")
        print(f"  [{c.chunk_index}] page={c.page_number} {preview!r}...")
    print(f"collection '{settings.chroma_collection}' now has {store.count()} chunks total")


def chat(args: argparse.Namespace) -> None:
    settings = get_settings()
    embedder = get_embedder(settings)
    store = get_vector_store(settings)
    llm = get_llm_client(settings)

    history: list[tuple[str, str]] = []
    for line in sys.stdin:
        question = line.strip()
        if not question:
            continue

        print(f"> {question}")
        answer = answer_question(question, history, settings, embedder, store, llm)
        if answer.standalone_question != question:
            print(f"(standalone: {answer.standalone_question})")
        print(answer.text)
        print("sources:")
        for i, c in enumerate(answer.sources, start=1):
            print(f"  [{i}] {c.metadata.get('source_file')} chunk={c.metadata.get('chunk_index')}")
        print()

        history.append((question, answer.text))


def main() -> None:
    parser = argparse.ArgumentParser(prog="rag-cli")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest_parser = sub.add_parser("ingest", help="parse, chunk, embed, and store a document")
    ingest_parser.add_argument("path")
    ingest_parser.set_defaults(func=ingest)

    chat_parser = sub.add_parser("chat", help="ask questions against the store, one per stdin line")
    chat_parser.set_defaults(func=chat)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
