# currently saved resume wapas dikhata hai

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "db"))
from db import get_connection


def get_resume():
    """
    Fetch the currently saved resume.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT content FROM resume WHERE id = 1")
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return "No resume saved yet. Use save_resume first."

    return row["content"]