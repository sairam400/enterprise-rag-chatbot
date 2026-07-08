"""Application configuration.

All runtime configuration is sourced from environment variables (or a local
``.env`` file) via :class:`Settings`. Every provider choice — LLM, embeddings,
and vector store — is toggled here so that swapping Anthropic for Azure OpenAI,
or ChromaDB for Azure AI Search, never requires a code change.

The repo runs for free out of the box: local ``sentence-transformers``
embeddings + local ChromaDB. Only an ``ANTHROPIC_API_KEY`` is required.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

LLMProvider = Literal["anthropic", "azure_openai"]
EmbeddingProvider = Literal["sentence_transformers", "azure_openai"]
VectorStoreProvider = Literal["chroma", "azure_search"]


class Settings(BaseSettings):
    """Strongly-typed application settings loaded from the environment.

    Field names map to upper-case environment variables (case-insensitive),
    e.g. ``anthropic_model`` reads ``ANTHROPIC_MODEL``.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- Provider selection ---------------------------------------------
    llm_provider: LLMProvider = "anthropic"
    embedding_provider: EmbeddingProvider = "sentence_transformers"
    vector_store: VectorStoreProvider = "chroma"

    # --- Anthropic (default LLM) ----------------------------------------
    anthropic_api_key: str | None = None
    # Default to current-generation Opus. For cheaper demos set
    # ANTHROPIC_MODEL=claude-sonnet-5 (near-Opus quality on grounded Q&A).
    anthropic_model: str = "claude-opus-4-8"
    anthropic_max_tokens: int = 2048

    # --- Azure OpenAI (optional LLM + embeddings) -----------------------
    azure_openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_api_version: str = "2024-10-21"
    azure_openai_chat_deployment: str | None = None
    azure_openai_embedding_deployment: str | None = None

    # --- Embeddings ------------------------------------------------------
    # Local default; runs on CPU, no API key needed.
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # --- ChromaDB (default vector store) --------------------------------
    chroma_persist_dir: str = "./data/chroma"
    chroma_collection: str = "documents"

    # --- Azure AI Search (optional vector store) ------------------------
    azure_search_endpoint: str | None = None
    azure_search_api_key: str | None = None
    azure_search_index: str = "documents"

    # --- Chunking --------------------------------------------------------
    chunk_size: int = 1000
    chunk_overlap: int = 150

    # --- Retrieval -------------------------------------------------------
    top_k: int = 5

    # --- App -------------------------------------------------------------
    max_upload_mb: int = 25
    # Comma-separated list of allowed CORS origins for the React dev server.
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        """CORS origins parsed into a list of trimmed, non-empty strings."""
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    def public_dict(self) -> dict[str, object]:
        """Return non-secret settings, safe to expose over the API.

        Secret fields (API keys) are reduced to a boolean "configured" flag so
        that a misconfiguration is diagnosable without leaking credentials.
        """
        return {
            "llm_provider": self.llm_provider,
            "embedding_provider": self.embedding_provider,
            "vector_store": self.vector_store,
            "anthropic_model": self.anthropic_model,
            "anthropic_max_tokens": self.anthropic_max_tokens,
            "anthropic_api_key_configured": self.anthropic_api_key is not None,
            "embedding_model": self.embedding_model,
            "chroma_collection": self.chroma_collection,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "top_k": self.top_k,
            "max_upload_mb": self.max_upload_mb,
        }


@lru_cache
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance (read once per process)."""
    return Settings()
