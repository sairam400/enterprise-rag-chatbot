"""FastAPI application entrypoint."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import chat, documents

settings = get_settings()

app = FastAPI(
    title="Enterprise RAG Chatbot",
    description="Document-grounded question answering with source citations.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router)
app.include_router(chat.router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/config", tags=["system"])
def config_view() -> dict[str, object]:
    """Active, non-secret settings for verifying deployment config."""
    return settings.public_dict()
