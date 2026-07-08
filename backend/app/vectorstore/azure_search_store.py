from .base import StoredChunk, VectorStore

# TODO: untested against a live Azure AI Search index, no Azure account in dev/CI.


class AzureSearchVectorStore(VectorStore):
    def __init__(self, endpoint: str, api_key: str, index_name: str):
        from azure.core.credentials import AzureKeyCredential
        from azure.search.documents import SearchClient

        self._client = SearchClient(endpoint, index_name, AzureKeyCredential(api_key))

    def add(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        texts: list[str],
        metadatas: list[dict[str, object]],
    ) -> None:
        documents = [
            {"id": i, "content": t, "content_vector": e, **m}
            for i, t, e, m in zip(ids, texts, embeddings, metadatas)
        ]
        self._client.upload_documents(documents)

    def query(self, embedding: list[float], top_k: int) -> list[StoredChunk]:
        from azure.search.documents.models import VectorizedQuery

        vector_query = VectorizedQuery(vector=embedding, k_nearest_neighbors=top_k, fields="content_vector")
        results = self._client.search(vector_queries=[vector_query], top=top_k)
        return [
            StoredChunk(
                id=r["id"],
                text=r["content"],
                metadata={k: v for k, v in r.items() if k not in ("id", "content", "content_vector")},
                distance=r.get("@search.score"),
            )
            for r in results
        ]

    def count(self) -> int:
        return self._client.get_document_count()
