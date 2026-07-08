from ..config import Settings
from .base import LLMClient


def get_llm_client(settings: Settings) -> LLMClient:
    if settings.llm_provider == "anthropic":
        from .anthropic_client import AnthropicClient

        if not settings.anthropic_api_key:
            raise ValueError("anthropic provider requires ANTHROPIC_API_KEY")
        return AnthropicClient(
            api_key=settings.anthropic_api_key,
            model=settings.anthropic_model,
            max_tokens=settings.anthropic_max_tokens,
        )

    if settings.llm_provider == "azure_openai":
        from .azure_openai_client import AzureOpenAIClient

        if not (settings.azure_openai_api_key and settings.azure_openai_endpoint):
            raise ValueError("azure_openai provider requires AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT")
        return AzureOpenAIClient(
            api_key=settings.azure_openai_api_key,
            endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
            deployment=settings.azure_openai_chat_deployment or "",
            max_tokens=settings.anthropic_max_tokens,
        )

    raise ValueError(f"unknown llm provider: {settings.llm_provider}")
