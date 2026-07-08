import argparse
from pathlib import Path

from .config import get_settings
from .embeddings import get_embedder
from .ingestion.pipeline import ingest_file
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


def main() -> None:
    parser = argparse.ArgumentParser(prog="rag-cli")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest_parser = sub.add_parser("ingest", help="parse, chunk, embed, and store a document")
    ingest_parser.add_argument("path")
    ingest_parser.set_defaults(func=ingest)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
