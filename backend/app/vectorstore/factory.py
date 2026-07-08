from ..config import Settings
from .base import VectorStore


def get_vector_store(settings: Settings) -> VectorStore:
    if settings.vector_store == "chroma":
        from .chroma_store import ChromaVectorStore

        return ChromaVectorStore(settings.chroma_persist_dir, settings.chroma_collection)

    if settings.vector_store == "azure_search":
        from .azure_search_store import AzureSearchVectorStore

        if not (settings.azure_search_endpoint and settings.azure_search_api_key):
            raise ValueError("azure_search requires AZURE_SEARCH_ENDPOINT and AZURE_SEARCH_API_KEY")
        return AzureSearchVectorStore(
            endpoint=settings.azure_search_endpoint,
            api_key=settings.azure_search_api_key,
            index_name=settings.azure_search_index,
        )

    raise ValueError(f"unknown vector store: {settings.vector_store}")
