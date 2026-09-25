import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "db"))
from db import get_connection


def track_topic(topic: str):
    """
    Mark that you've revised a topic (independent of where the note lives —
    just tracks how many times you've revisited each topic).
    """
    conn = get_connection()
    cursor = conn.cursor()

    # INSERT ... ON CONFLICT: create the row if it's new, otherwise +1 the count
    cursor.execute(
        """
        INSERT INTO topic_tracking (topic, revisit_count)
        VALUES (?, 1)
        ON CONFLICT(topic) DO UPDATE SET revisit_count = revisit_count + 1
        """,
        (topic,),
    )
    conn.commit()

    cursor.execute("SELECT revisit_count FROM topic_tracking WHERE topic = ?", (topic,))
    count = cursor.fetchone()["revisit_count"]
    conn.close()

    return f"'{topic}' revisited {count} time(s) so far."