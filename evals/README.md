# Evaluation Harness

Measures **retrieval hit rate** (is the correct chunk in top-k?) and **answer
faithfulness** (LLM-as-judge: is the answer supported by the retrieved
context?) over a small labelled dataset, and emits a Markdown results table for
the top-level README. **Added in Phase 6.**
