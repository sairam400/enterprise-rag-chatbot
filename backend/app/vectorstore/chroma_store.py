from .base import StoredChunk, VectorStore


class ChromaVectorStore(VectorStore):
    def __init__(self, persist_dir: str, collection_name: str):
        import chromadb

        client = chromadb.PersistentClient(path=persist_dir)
        self._collection = client.get_or_create_collection(collection_name)

    def add(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        texts: list[str],
        metadatas: list[dict[str, object]],
    ) -> None:
        self._collection.upsert(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)

    def query(self, embedding: list[float], top_k: int) -> list[StoredChunk]:
        result = self._collection.query(query_embeddings=[embedding], n_results=top_k)
        ids = result["ids"][0]
        documents = result["documents"][0]
        metadatas = result["metadatas"][0]
        distances = result["distances"][0]
        return [
            StoredChunk(id=i, text=d, metadata=m, distance=dist)
            for i, d, m, dist in zip(ids, documents, metadatas, distances)
        ]

    def count(self) -> int:
        return self._collection.count()
