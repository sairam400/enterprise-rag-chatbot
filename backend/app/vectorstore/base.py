from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class StoredChunk:
    id: str
    text: str
    metadata: dict[str, object]
    distance: float | None = None


class VectorStore(ABC):
    @abstractmethod
    def add(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        texts: list[str],
        metadatas: list[dict[str, object]],
    ) -> None: ...

    @abstractmethod
    def query(self, embedding: list[float], top_k: int) -> list[StoredChunk]: ...

    @abstractmethod
    def count(self) -> int: ...
