import sys
import os
from pypdf import PdfReader
from docx import Document

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "db"))
from db import get_connection


def _extract_from_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def _extract_from_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def import_resume_pdf(pdf_path: str):
    """
    Read a resume file from disk (PDF or DOCX), extract its text,
    and save it as the base resume.
    """
    if not os.path.exists(pdf_path):
        return f"File not found: {pdf_path}"

    ext = os.path.splitext(pdf_path)[1].lower()

    if ext == ".pdf":
        text = _extract_from_pdf(pdf_path)
    elif ext == ".docx":
        text = _extract_from_docx(pdf_path)
    else:
        return f"Unsupported file type '{ext}'. Please provide a .pdf or .docx file."

    if not text.strip():
        return "Could not extract any text from this file."

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO resume (id, content) VALUES (1, ?)", (text,))
    conn.commit()
    conn.close()

    return "Resume imported and saved."