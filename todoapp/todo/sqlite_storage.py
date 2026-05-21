# Transitional SQLite storage that stores the whole app state as one JSON blob.
# Kept for learning/comparison.

import json
import sqlite3
from pathlib import Path
from typing import Optional


class SqliteStorage:
    """
    Ugyanaz a szerződés, mint JsonStorage:
    - load_dict() -> dict
    - save_dict(data) -> None
    Belül SQLite-ben tárol egyetlen JSON blobot.
    """

    def __init__(self, filename: str = "todo.db") -> None:
        p = Path(filename)

        if p.is_absolute() or len(p.parts) > 1:
            self.path = p
        else:

            self.path = Path(__file__).with_name(filename)

        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _init_db(self) -> None:
        with self._connect() as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS kv (
                    k TEXT PRIMARY KEY,
                    v TEXT NOT NULL
                )
            """)

            cur = con.execute("SELECT v FROM kv WHERE k='state'")
            row = cur.fetchone()
            if row is None:
                con.execute(
                    "INSERT INTO kv(k, v) VALUES('state', ?)", (json.dumps({}),))

    def load_dict(self) -> dict:
        with self._connect() as con:
            cur = con.execute("SELECT v FROM kv WHERE k='state'")
            row = cur.fetchone()
            if row is None:
                return {}
            raw = row[0]
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                return {}
            return data if isinstance(data, dict) else {}

    def save_dict(self, data: dict) -> None:
        raw = json.dumps(data, ensure_ascii=False, indent=2)
        with self._connect() as con:
            con.execute("UPDATE kv SET v=? WHERE k='state'", (raw,))
