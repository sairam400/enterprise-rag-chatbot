from dataclasses import dataclass

from ..config import Settings
from ..embeddings import Embedder
from ..llm import LLMClient
from ..vectorstore import StoredChunk, VectorStore
from .prompt import SYSTEM_PROMPT, build_user_prompt
from .query_rewrite import rewrite_query


@dataclass
class Answer:
    text: str
    standalone_question: str
    sources: list[StoredChunk]


def answer_question(
    question: str,
    history: list[tuple[str, str]],
    settings: Settings,
    embedder: Embedder,
    store: VectorStore,
    llm: LLMClient,
) -> Answer:
    standalone = rewrite_query(llm, history, question)

    [embedding] = embedder.embed([standalone])
    chunks = store.query(embedding, settings.top_k)

    text = llm.complete(SYSTEM_PROMPT, build_user_prompt(standalone, chunks))
    return Answer(text=text, standalone_question=standalone, sources=chunks)
