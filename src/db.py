import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/courses.db")

def init_db():
    """Creates the database and table if they don't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS course_status (
            code        TEXT PRIMARY KEY,
            name        TEXT,
            status      TEXT,
            enrolled    TEXT,
            waitlist    TEXT,
            last_checked TEXT,
            notified    INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def get_last_status(course_code: str) -> str | None:
    """Returns the last known status for a course, or None if unseen."""
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT status FROM course_status WHERE code = ?", (course_code,)
    ).fetchone()
    conn.close()
    return row[0] if row else None


def upsert_course(data: dict, name: str, notified: int = 0):
    """Inserts or updates a course record."""
    from datetime import datetime
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO course_status (code, name, status, enrolled, waitlist, last_checked, notified)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(code) DO UPDATE SET
            status=excluded.status,
            enrolled=excluded.enrolled,
            waitlist=excluded.waitlist,
            last_checked=excluded.last_checked,
            notified=excluded.notified
    """, (
        data["code"], name, data["status"],
        data["enrolled"], data.get("waitlist", "N/A"),
        datetime.now().isoformat(), notified
    ))
    conn.commit()
    conn.close()


def was_notified(course_code: str) -> bool:
    """Returns True if we already sent a notification for this course opening."""
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT notified FROM course_status WHERE code = ?", (course_code,)
    ).fetchone()
    conn.close()
    return bool(row[0]) if row else False
