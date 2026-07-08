from ..llm import LLMClient

REWRITE_SYSTEM = (
    "Rewrite the latest user question into a standalone question that makes sense "
    "without the conversation history. Preserve the original intent. Reply with only "
    "the rewritten question, nothing else."
)


def rewrite_query(llm: LLMClient, history: list[tuple[str, str]], question: str) -> str:
    if not history:
        return question

    turns = "\n".join(f"User: {q}\nAssistant: {a}" for q, a in history)
    user = f"Conversation so far:\n{turns}\n\nLatest question: {question}\n\nStandalone question:"
    return llm.complete(REWRITE_SYSTEM, user).strip()
