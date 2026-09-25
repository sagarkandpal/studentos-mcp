import sys
import os

sys.path.append(os.path.dirname(__file__))
from drive_helper import search_drive_notes


def search_notes(query: str):
    """Search the student's Google Drive notes by name or content."""
    return search_drive_notes(query)