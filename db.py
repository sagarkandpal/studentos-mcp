import sqlite3
import os

# paths relative to this file, so it works no matter where you run python from
CURRENT_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(CURRENT_DIR, "notes.db")
SCHEMA_PATH = os.path.join(CURRENT_DIR, "schema.sql")


def get_connection():
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us access columns by name, e.g. row["topic"]
    return conn


def init_db():
    """Create the notes table (and seed sample data) if the DB doesn't exist yet."""
    if not os.path.exists(DB_PATH):
        conn = get_connection()
        with open(SCHEMA_PATH, "r") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Database created and seeded with sample notes.")