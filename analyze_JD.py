# kisi JD ka text leke Gemini se uske key requirements/skills bullet points mein nikalwata hai

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# a fresh, small Groq model just for this one task — extracting key info from a JD
_model = ChatGroq(model="openai/gpt-oss-20b")


def analyze_jd(jd_text: str):
    """
    Read a job description and pull out the key skills/requirements
    it's asking for, as a short bullet list.
    """
    prompt = (
        "Read this job description and list only the key skills and "
        "requirements it asks for, as short bullet points:\n\n"
        f"{jd_text}"
    )
    response = _model.invoke(prompt)

    # Gemini sometimes returns content as a list of blocks instead of a plain string.
    # Same defensive pattern used in chatbot.py — pull out just the text parts.
    content = response.content
    if isinstance(content, list):
        return "".join(block.get("text", "") for block in content if isinstance(block, dict))
    return content