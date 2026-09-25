# base resume + ab tak ke saare logged skills + di gayi JD, teeno ko combine karke Gemini se ek naya, us JD ke hisab se tailored resume bana deta hai

import sys
import os
import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from fpdf import FPDF

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "db"))
from db import get_connection

load_dotenv()
_model = ChatGroq(model="openai/gpt-oss-20b")

# where generated PDFs get saved
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")


def _save_as_pdf(text: str):
    """Turn plain text into a simple PDF file and return its path."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tailored_resume_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)

    # Helvetica only supports basic latin characters, so we strip anything else
    safe_text = text.encode("latin-1", errors="ignore").decode("latin-1")
    pdf.multi_cell(0, 8, safe_text)
    pdf.output(filepath)

    return filepath


def generate_tailored_resume(jd_text: str):
    """
    Combine the base resume + everything the student has learned (skills_log)
    with a job description, produce a tailored resume, and save it as a PDF.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT content FROM resume WHERE id = 1")
    row = cursor.fetchone()
    base_resume = row["content"] if row else ""

    cursor.execute("SELECT skill FROM skills_log ORDER BY learned_at")
    skills = [r["skill"] for r in cursor.fetchall()]
    conn.close()

    if not base_resume:
        return "No base resume saved yet. Use save_resume or import_resume_pdf first."

    skills_text = ", ".join(skills) if skills else "None logged yet."

    prompt = (
        "You are helping a student tailor their resume for a specific job.\n\n"
        f"BASE RESUME:\n{base_resume}\n\n"
        f"ADDITIONAL SKILLS THE STUDENT HAS LEARNED SINCE:\n{skills_text}\n\n"
        f"JOB DESCRIPTION:\n{jd_text}\n\n"
        "Rewrite the resume so it highlights the most relevant base resume "
        "content AND the additional skills that match this job description. "
        "Keep it concise and in resume format."
    )

    response = _model.invoke(prompt)

    # Gemini sometimes returns content as a list of blocks instead of a plain string.
    # _save_as_pdf() needs a real string — same defensive pattern as chatbot.py.
    content = response.content
    if isinstance(content, list):
        tailored_text = "".join(block.get("text", "") for block in content if isinstance(block, dict))
    else:
        tailored_text = content

    pdf_path = _save_as_pdf(tailored_text)

    return f"Tailored resume generated and saved as PDF at: {pdf_path}\n\n{tailored_text}"