import hashlib
from pathlib import Path

from ..config import Settings
from ..embeddings import Embedder
from ..vectorstore import VectorStore
from .chunker import chunk_pages
from .models import Chunk
from .parsers import parse


def ingest_file(path: Path, settings: Settings, embedder: Embedder, store: VectorStore) -> list[Chunk]:
    pages = parse(path)
    chunks = chunk_pages(pages, source_file=path.name, chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
    if not chunks:
        return []

    embeddings = embedder.embed([c.text for c in chunks])
    ids = [_chunk_id(path.name, c.chunk_index) for c in chunks]
    metadatas = [
        {"source_file": c.source_file, "chunk_index": c.chunk_index, "page_number": c.page_number or 0}
        for c in chunks
    ]
    store.add(ids=ids, embeddings=embeddings, texts=[c.text for c in chunks], metadatas=metadatas)
    return chunks


def _chunk_id(source_file: str, chunk_index: int) -> str:
    digest = hashlib.sha1(source_file.encode("utf-8")).hexdigest()[:12]
    return f"{digest}-{chunk_index}"
