import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "studyai.db"


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                idea TEXT NOT NULL,
                artifacts TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                score INTEGER NOT NULL,
                comments TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT NOT NULL,
                details TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def save_session(session_id: str, created_at: str, idea: str, artifacts: dict) -> None:
    with _conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO sessions (session_id, created_at, idea, artifacts) VALUES (?, ?, ?, ?)",
            (session_id, created_at, idea, json.dumps(artifacts)),
        )


def get_session(session_id: str) -> dict | None:
    with _conn() as conn:
        row = conn.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,)).fetchone()
        if not row:
            return None
        return {
            "session_id": row["session_id"],
            "created_at": row["created_at"],
            "idea": row["idea"],
            "artifacts": json.loads(row["artifacts"]),
        }


def save_feedback(session_id: str, score: int, comments: str | None, created_at: str) -> None:
    with _conn() as conn:
        conn.execute(
            "INSERT INTO feedback (session_id, score, comments, created_at) VALUES (?, ?, ?, ?)",
            (session_id, score, comments, created_at),
        )


def save_audit(event: str, details: dict, created_at: str) -> None:
    with _conn() as conn:
        conn.execute(
            "INSERT INTO audit_logs (event, details, created_at) VALUES (?, ?, ?)",
            (event, json.dumps(details), created_at),
        )
