from ..config import Settings
from .base import Embedder


def get_embedder(settings: Settings) -> Embedder:
    if settings.embedding_provider == "sentence_transformers":
        from .sentence_transformers_embedder import SentenceTransformerEmbedder

        return SentenceTransformerEmbedder(settings.embedding_model)

    if settings.embedding_provider == "azure_openai":
        from .azure_openai_embedder import AzureOpenAIEmbedder

        if not (settings.azure_openai_api_key and settings.azure_openai_endpoint):
            raise ValueError("azure_openai embeddings require AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT")
        return AzureOpenAIEmbedder(
            api_key=settings.azure_openai_api_key,
            endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
            deployment=settings.azure_openai_embedding_deployment or "",
        )

    raise ValueError(f"unknown embedding provider: {settings.embedding_provider}")
