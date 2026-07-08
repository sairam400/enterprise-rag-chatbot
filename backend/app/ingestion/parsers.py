from pathlib import Path

from .models import Page

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}


def parse(path: Path) -> list[Page]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _parse_pdf(path)
    if suffix == ".docx":
        return _parse_docx(path)
    if suffix in (".txt", ".md"):
        return _parse_text(path)
    raise ValueError(f"unsupported file type: {suffix}")


def _parse_pdf(path: Path) -> list[Page]:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    return [Page(text=p.extract_text() or "", page_number=i + 1) for i, p in enumerate(reader.pages)]


def _parse_docx(path: Path) -> list[Page]:
    import docx

    doc = docx.Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs)
    return [Page(text=text, page_number=None)]


def _parse_text(path: Path) -> list[Page]:
    return [Page(text=path.read_text(encoding="utf-8"), page_number=None)]
