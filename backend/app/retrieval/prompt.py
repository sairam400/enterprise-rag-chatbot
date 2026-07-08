from ..vectorstore import StoredChunk

SYSTEM_PROMPT = """You are a document question-answering assistant. Answer only using the \
numbered context passages given below. Cite the passages you relied on with bracketed \
numbers inline, like [1] or [1][2]. If the passages do not contain the answer, say plainly \
that the documents don't cover it. Do not use outside knowledge."""


def build_context(chunks: list[StoredChunk]) -> str:
    blocks = []
    for i, c in enumerate(chunks, start=1):
        source = c.metadata.get("source_file", "unknown")
        blocks.append(f"[{i}] (source: {source})\n{c.text}")
    return "\n\n".join(blocks)


def build_user_prompt(question: str, chunks: list[StoredChunk]) -> str:
    return f"Context passages:\n\n{build_context(chunks)}\n\nQuestion: {question}"
