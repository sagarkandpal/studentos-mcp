import sys
import os

sys.path.append(os.path.dirname(__file__))
from drive_helper import find_file_by_name, get_drive_file_content


def read_note(note_name: str):
    """Read the full content of a Drive note, given its name (e.g. 'Lecture 3 Notes')."""
    # Step 1: find the Drive file whose name matches what the user typed
    file = find_file_by_name(note_name)
    if file is None:
        return f"No Drive file found matching '{note_name}'. Try search_notes first to see exact names."

    # Step 2: now that we have the real Drive file id, download and return the content
    return get_drive_file_content(file["id"])