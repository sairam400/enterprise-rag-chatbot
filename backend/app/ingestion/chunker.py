from .models import Chunk, Page

# Split on paragraph, then line, then sentence, then word, in that order of
# preference, so chunks break on natural boundaries rather than mid-sentence.
SEPARATORS = ["\n\n", "\n", ". ", " "]


def chunk_pages(pages: list[Page], source_file: str, chunk_size: int, chunk_overlap: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    for page in pages:
        for piece in _split(page.text, chunk_size, SEPARATORS):
            piece = piece.strip()
            if piece:
                chunks.append(
                    Chunk(text=piece, chunk_index=len(chunks), source_file=source_file, page_number=page.page_number)
                )
    return _apply_overlap(chunks, chunk_overlap)


def _split(text: str, chunk_size: int, separators: list[str]) -> list[str]:
    if len(text) <= chunk_size:
        return [text] if text else []

    if not separators:
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    sep, rest = separators[0], separators[1:]
    parts = text.split(sep)

    pieces: list[str] = []
    current = ""
    for part in parts:
        candidate = current + sep + part if current else part
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                pieces.append(current)
            current = part if len(part) <= chunk_size else ""
            if not current and part:
                pieces.extend(_split(part, chunk_size, rest))
    if current:
        pieces.append(current)
    return pieces


def _apply_overlap(chunks: list[Chunk], overlap: int) -> list[Chunk]:
    if overlap <= 0 or len(chunks) < 2:
        return chunks

    overlapped = [chunks[0]]
    for prev, curr in zip(chunks, chunks[1:]):
        prefix = prev.text[-overlap:]
        overlapped.append(
            Chunk(
                text=f"{prefix} {curr.text}",
                chunk_index=curr.chunk_index,
                source_file=curr.source_file,
                page_number=curr.page_number,
            )
        )
    return overlapped
