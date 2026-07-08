from .schemas import DocumentInfo

# In-memory, process-lifetime only. Fine for a single-worker demo deployment;
# a real deployment would move this to Redis or a database.
documents: list[DocumentInfo] = []
conversations: dict[str, list[tuple[str, str]]] = {}
