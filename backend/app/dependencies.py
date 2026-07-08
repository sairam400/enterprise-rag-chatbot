from functools import lru_cache

from .config import get_settings
from .embeddings import Embedder
from .embeddings import get_embedder as _get_embedder
from .llm import LLMClient
from .llm import get_llm_client as _get_llm_client
from .vectorstore import VectorStore
from .vectorstore import get_vector_store as _get_vector_store


@lru_cache
def embedder() -> Embedder:
    return _get_embedder(get_settings())


@lru_cache
def vector_store() -> VectorStore:
    return _get_vector_store(get_settings())


@lru_cache
def llm_client() -> LLMClient:
    return _get_llm_client(get_settings())
