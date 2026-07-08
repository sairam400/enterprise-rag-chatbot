"""Runs dataset.json through the real retrieval + generation pipeline and
scores retrieval hit rate and answer faithfulness (LLM-as-judge). Writes
results.md.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.config import get_settings  # noqa: E402
from app.embeddings import get_embedder  # noqa: E402
from app.ingestion.pipeline import ingest_file  # noqa: E402
from app.llm import get_llm_client  # noqa: E402
from app.retrieval.pipeline import answer_question  # noqa: E402
from app.retrieval.prompt import build_context  # noqa: E402
from app.vectorstore import get_vector_store  # noqa: E402

SAMPLE_DOCS = ROOT / "sample_docs"
EVAL_DIR = Path(__file__).resolve().parent
RESULTS_PATH = EVAL_DIR / "results.md"

JUDGE_SYSTEM = (
    "You are grading whether an AI assistant's answer is faithful to the given "
    "context. Faithful means every claim in the answer is supported by the "
    "context, or the context does not contain the answer and the assistant "
    "correctly said so instead of guessing. Respond with exactly one word, PASS "
    "or FAIL, then a dash and a one-sentence reason."
)


def judge_prompt(question: str, context: str, answer: str) -> str:
    return f"Context:\n{context}\n\nQuestion: {question}\n\nAssistant's answer: {answer}\n\nVerdict:"


def main() -> None:
    settings = get_settings().model_copy(
        update={
            "chroma_persist_dir": str(EVAL_DIR / "eval_data" / "chroma"),
            "chroma_collection": "eval_documents",
        }
    )
    embedder = get_embedder(settings)
    store = get_vector_store(settings)
    llm = get_llm_client(settings)

    for path in sorted(SAMPLE_DOCS.glob("*")):
        if path.name == "README.md" or path.suffix.lower() not in {".pdf", ".docx", ".txt", ".md"}:
            continue
        chunks = ingest_file(path, settings, embedder, store)
        print(f"ingested {path.name}: {len(chunks)} chunks")

    dataset = json.loads((EVAL_DIR / "dataset.json").read_text())

    rows = []
    for item in dataset:
        answer = answer_question(item["question"], [], settings, embedder, store, llm)
        sources = [c.metadata.get("source_file") for c in answer.sources]

        hit = item["expected_source_file"] in sources if item["answerable"] else None

        context = build_context(answer.sources)
        verdict_response = llm.complete(JUDGE_SYSTEM, judge_prompt(item["question"], context, answer.text))
        faithful = verdict_response.strip().upper().startswith("PASS")

        rows.append(
            {
                "id": item["id"],
                "question": item["question"],
                "answerable": item["answerable"],
                "retrieval_hit": hit,
                "faithful": faithful,
            }
        )
        print(f"[{item['id']}] hit={hit} faithful={faithful}")

    answerable = [r for r in rows if r["answerable"]]
    hit_rate = sum(1 for r in answerable if r["retrieval_hit"]) / len(answerable)
    faithfulness_rate = sum(1 for r in rows if r["faithful"]) / len(rows)

    write_results(rows, hit_rate, faithfulness_rate, settings)
    print(f"\nretrieval hit rate: {hit_rate:.0%}")
    print(f"faithfulness rate: {faithfulness_rate:.0%}")


def write_results(rows: list[dict], hit_rate: float, faithfulness_rate: float, settings) -> None:
    answerable = [r for r in rows if r["answerable"]]
    lines = [
        "# Evaluation Results",
        "",
        f"Model: `{settings.anthropic_model}` &middot; Embeddings: `{settings.embedding_model}` &middot; top_k: {settings.top_k}",
        "",
        f"**Retrieval hit rate:** {hit_rate:.0%} "
        f"({sum(1 for r in answerable if r['retrieval_hit'])}/{len(answerable)} answerable questions)",
        f"**Answer faithfulness:** {faithfulness_rate:.0%} "
        f"({sum(1 for r in rows if r['faithful'])}/{len(rows)} questions, includes correct abstentions)",
        "",
        "| ID | Question | Answerable | Retrieval Hit | Faithful |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        hit_display = "-" if r["retrieval_hit"] is None else ("yes" if r["retrieval_hit"] else "no")
        lines.append(
            f"| {r['id']} | {r['question']} | {'yes' if r['answerable'] else 'no'} "
            f"| {hit_display} | {'yes' if r['faithful'] else 'no'} |"
        )
    RESULTS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
