from dataclasses import dataclass


@dataclass
class Page:
    text: str
    page_number: int | None = None


@dataclass
class Chunk:
    text: str
    chunk_index: int
    source_file: str
    page_number: int | None = None
