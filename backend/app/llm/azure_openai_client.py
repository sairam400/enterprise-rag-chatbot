from .base import LLMClient

# TODO: untested against a live Azure endpoint, no Azure account in dev/CI.


class AzureOpenAIClient(LLMClient):
    def __init__(self, api_key: str, endpoint: str, api_version: str, deployment: str, max_tokens: int):
        from openai import AzureOpenAI

        self._client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=api_version)
        self._deployment = deployment
        self._max_tokens = max_tokens

    def complete(self, system: str, user: str) -> str:
        response = self._client.chat.completions.create(
            model=self._deployment,
            max_tokens=self._max_tokens,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        return response.choices[0].message.content or ""
