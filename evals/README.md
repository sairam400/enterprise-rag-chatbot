# Evaluation Harness

Measures retrieval hit rate (is the right document in the top-k retrieved
chunks?) and answer faithfulness (LLM-as-judge: is the answer supported by
the retrieved context, or a correct abstention?) against `dataset.json`, a
14-question set over the docs in [`/sample_docs`](../sample_docs).

```bash
cd backend && pip install -r requirements.txt   # if not already done
cd .. && backend/.venv/Scripts/python evals/run_eval.py     # backend/venv/bin/python on Linux/Mac
```

Requires a real `ANTHROPIC_API_KEY` in `backend/.env` since the judge is a
second Claude call. Writes `results.md` here; that table gets pasted into the
top-level README.

`generate_sample_docs.py` is the one-time script that produced
`onboarding_guide.docx` and `product_faq.pdf`. It needs `reportlab`
(`pip install -r requirements.txt` in this directory) and only needs to be
re-run if you want to regenerate those two files from scratch.
