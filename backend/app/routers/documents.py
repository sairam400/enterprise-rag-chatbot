import tempfile
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from .. import state
from ..config import get_settings
from ..dependencies import embedder, vector_store
from ..ingestion.parsers import SUPPORTED_EXTENSIONS
from ..ingestion.pipeline import ingest_file
from ..schemas import DocumentInfo

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("", response_model=DocumentInfo)
async def upload_document(file: UploadFile) -> DocumentInfo:
    if not file.filename:
        raise HTTPException(400, "missing filename")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(400, f"unsupported file type: {suffix}")

    settings = get_settings()
    contents = await file.read()
    if len(contents) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(400, f"file exceeds {settings.max_upload_mb}MB limit")

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / file.filename
        path.write_bytes(contents)
        chunks = await run_in_threadpool(ingest_file, path, settings, embedder(), vector_store())

    info = DocumentInfo(filename=file.filename, chunks=len(chunks))
    state.documents.append(info)
    return info


@router.get("", response_model=list[DocumentInfo])
def list_documents() -> list[DocumentInfo]:
    return state.documents
