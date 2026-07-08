# Known Issues

## Phase 7: docker-compose full-stack verification incomplete

`docker-compose up --build` has not been confirmed working end to end yet.

What happened: the first build attempt succeeded in pulling images but showed
the backend image installing torch's full CUDA/GPU build (~2GB of unused
NVIDIA libraries) even though the embedding model only ever runs on CPU here.
Fixed by installing a CPU-only torch wheel explicitly in
`backend/Dockerfile` before the rest of `requirements.txt`:

```dockerfile
RUN pip install --timeout 120 --retries 5 torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --timeout 120 --retries 5 -r requirements.txt
```

The rebuild after that fix hit a `ReadTimeoutError` against
`download-r2.pytorch.org` partway through (flaky network in the dev
environment, not a code issue). A second rebuild attempt was in progress,
further along than the first, when work paused for a system restart.

**Next step:** re-run `docker compose up --build -d` from the repo root,
confirm all containers report healthy, and curl `/health`, `/api/config`,
`/api/documents`, and `/api/chat` against the containerized backend, then
open `http://localhost:5173` and confirm the frontend talks to it. If it
passes, delete this file and mark Phase 7 done in the README roadmap.

Everything through Phase 6 (ingestion, retrieval + citations, FastAPI
endpoints, React frontend, eval harness) has been verified running directly
(outside Docker) and is committed and pushed.
