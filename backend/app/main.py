"""FastAPI application entrypoint.

Phase 1 exposes only health and config introspection so the container is
verifiable end-to-end (``docker-compose up`` → ``GET /health``). Ingestion,
retrieval, and chat endpoints are added in later phases.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings

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


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Liveness probe. Returns ``{"status": "ok"}`` when the app is up."""
    return {"status": "ok"}


@app.get("/api/config", tags=["system"])
def config_view() -> dict[str, object]:
    """Return the active, non-secret configuration for verification/debugging."""
    return settings.public_dict()
