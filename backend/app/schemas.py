from pydantic import BaseModel


class DocumentInfo(BaseModel):
    filename: str
    chunks: int


class SourceChunk(BaseModel):
    index: int
    source_file: str
    chunk_index: int
    page_number: int | None
    text: str


class ChatRequest(BaseModel):
    question: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    conversation_id: str
    standalone_question: str
    answer: str
    sources: list[SourceChunk]
