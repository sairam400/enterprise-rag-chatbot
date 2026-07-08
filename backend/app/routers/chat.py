import uuid

from fastapi import APIRouter
from starlette.concurrency import run_in_threadpool

from .. import state
from ..config import get_settings
from ..dependencies import embedder, llm_client, vector_store
from ..retrieval.pipeline import answer_question
from ..schemas import ChatRequest, ChatResponse, SourceChunk

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    conversation_id = request.conversation_id or str(uuid.uuid4())
    history = state.conversations.setdefault(conversation_id, [])

    answer = await run_in_threadpool(
        answer_question,
        request.question,
        history,
        get_settings(),
        embedder(),
        vector_store(),
        llm_client(),
    )
    history.append((request.question, answer.text))

    sources = [
        SourceChunk(
            index=i,
            source_file=str(c.metadata.get("source_file")),
            chunk_index=int(c.metadata.get("chunk_index", 0)),
            page_number=c.metadata.get("page_number") or None,
            text=c.text,
        )
        for i, c in enumerate(answer.sources, start=1)
    ]
    return ChatResponse(
        conversation_id=conversation_id,
        standalone_question=answer.standalone_question,
        answer=answer.text,
        sources=sources,
    )
