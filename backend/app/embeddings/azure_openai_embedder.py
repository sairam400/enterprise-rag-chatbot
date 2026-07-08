from .base import Embedder

# TODO: untested against a live Azure endpoint, no Azure account in dev/CI.


class AzureOpenAIEmbedder(Embedder):
    def __init__(self, api_key: str, endpoint: str, api_version: str, deployment: str):
        from openai import AzureOpenAI

        self._client = AzureOpenAI(
            api_key=api_key, azure_endpoint=endpoint, api_version=api_version
        )
        self._deployment = deployment

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = self._client.embeddings.create(input=texts, model=self._deployment)
        return [item.embedding for item in response.data]
