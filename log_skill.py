# jab bhi kuch naya seekho, wo entry skills_log table mein add karta hai

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "db"))
from db import get_connection


def log_skill(skill: str):
    """
    Record that the student learned something new.
    Just appends to skills_log — we never delete old entries.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO skills_log (skill) VALUES (?)", (skill,))
    conn.commit()
    conn.close()

    return f"Logged new skill: '{skill}'."