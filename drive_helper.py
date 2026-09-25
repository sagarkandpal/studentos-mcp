import sys
import os
import io
from pypdf import PdfReader
from docx import Document

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "auth"))
from google_auth import get_drive_service

GOOGLE_DOC_MIME = "application/vnd.google-apps.document"
PDF_MIME = "application/pdf"
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def _raw_search(query: str):
    """Just hits the Drive API and returns raw file matches (id, name, mimeType, link)."""
    service = get_drive_service()

    safe_query = query.replace("'", "")
    drive_query = (
        f"fullText contains '{safe_query}' and trashed = false and "
        f"(mimeType = '{GOOGLE_DOC_MIME}' or mimeType = '{PDF_MIME}' or mimeType = '{DOCX_MIME}')"
    )

    results = service.files().list(
        q=drive_query,
        fields="files(id, name, mimeType, webViewLink)",
        pageSize=10,
    ).execute()

    return results.get("files", [])


def get_drive_file_content(file_id: str, max_chars: int = 5000):
    """
    Download and extract the text content of a Drive file,
    handling Google Docs, PDF, and DOCX differently.
    Capped at max_chars so huge notes don't overload the conversation —
    still plenty for answering a specific question about the note.
    """
    service = get_drive_service()

    metadata = service.files().get(fileId=file_id, fields="name, mimeType").execute()
    mime_type = metadata["mimeType"]

    if mime_type == GOOGLE_DOC_MIME:
        raw = service.files().export_media(fileId=file_id, mimeType="text/plain").execute()
        text = raw.decode("utf-8")

    elif mime_type == PDF_MIME:
        raw = service.files().get_media(fileId=file_id).execute()
        reader = PdfReader(io.BytesIO(raw))
        text = "\n".join(page.extract_text() for page in reader.pages)

    elif mime_type == DOCX_MIME:
        raw = service.files().get_media(fileId=file_id).execute()
        doc = Document(io.BytesIO(raw))
        text = "\n".join(p.text for p in doc.paragraphs)

    else:
        return f"Unsupported file type: {mime_type}"

    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[Note truncated — this file is longer than shown. Ask a more specific question to dig into a particular part.]"

    return text


def search_drive_notes(query: str):
    """
    Search Drive and return each match's name + a clickable link to open it.
    We do NOT download/preview content here — that would be slow and
    pointless for long notes. The student just opens the link themselves.
    """
    files = _raw_search(query)
    if not files:
        return "No matching notes found in Drive."

    return [
        {"name": f["name"], "link": f["webViewLink"]}
        for f in files
    ]


def find_file_by_name(name: str):
    """
    Used by read_note: find the Drive file whose name best matches
    what the user typed, so they never have to give a raw file id.
    """
    files = _raw_search(name)
    if not files:
        return None

    for f in files:
        if f["name"].lower() == name.lower():
            return f

    return files[0]