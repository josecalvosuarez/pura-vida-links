"""SQLite repository (T008) — FR-010. Schema from data-model.md."""
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

SCHEMA = """
CREATE TABLE IF NOT EXISTS links (
    code       TEXT PRIMARY KEY,
    url        TEXT NOT NULL,
    created_at TEXT NOT NULL
)
"""


class DuplicateCode(Exception):
    """The code (random or alias) already exists — FR-007."""


@dataclass(frozen=True)
class Link:
    code: str
    url: str
    created_at: str


class LinkStore:
    def __init__(self, db_path: str | Path):
        self._conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._lock = Lock()
        with self._lock, self._conn:
            self._conn.execute(SCHEMA)

    def insert(self, code: str, url: str) -> Link:
        link = Link(code, url, datetime.now(timezone.utc).isoformat(timespec="seconds"))
        try:
            with self._lock, self._conn:
                self._conn.execute(
                    "INSERT INTO links (code, url, created_at) VALUES (?, ?, ?)",
                    (link.code, link.url, link.created_at),
                )
        except sqlite3.IntegrityError as exc:
            raise DuplicateCode(code) from exc
        return link

    def get(self, code: str) -> Link | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT code, url, created_at FROM links WHERE code = ?", (code,)
            ).fetchone()
        return Link(*row) if row else None

    def close(self) -> None:
        self._conn.close()
