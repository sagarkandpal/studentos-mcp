#student ka base resume ek baar save/update karta hai DB mein

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "db"))
from db import get_connection


def save_resume(resume_text: str):
    """
    Save (or overwrite) the student's base resume.
    We only ever keep one resume, so we always use id = 1.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # "INSERT OR REPLACE" means: if a row with id=1 exists, overwrite it; else create it.
    cursor.execute(
        "INSERT OR REPLACE INTO resume (id, content) VALUES (1, ?)",
        (resume_text,),
    )
    conn.commit()
    conn.close()

    return "Resume saved."