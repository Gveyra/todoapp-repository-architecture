# Main storage implementation for the app.
# Stores todo items in real SQLite tables (items + meta).

import sqlite3
from pathlib import Path


class SqliteTableStorage:
    def __init__(self, filename: str = "todo_table.db") -> None:
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
                CREATE TABLE IF NOT EXISTS items(
                    id INTEGER PRIMARY KEY,
                    text TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    done INTEGER NOT NULL
                  )
                """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS meta(
                    key TEXT PRIMARY KEY, 
                    value TEXT NOT NULL
                    )
                """)
            cur = con.execute("SELECT value FROM meta WHERE key = 'next_id'")
            row = cur.fetchone()
            if row is None:
                con.execute(
                    "INSERT INTO meta(key, value) VALUES('next_id', '1')")

    def load_dict(self) -> dict:
        with self._connect() as con:
            # items lekérése:
            cur = con.execute("""
                SELECT id, text, priority, done
                FROM items
                ORDER BY id
            """)
            rows = cur.fetchall()

            items = []
            for row in rows:
                items.append(
                    {
                        "id": int(row[0]),
                        "text": str(row[1]),
                        "priority": int(row[2]),
                        "done": bool(row[3]),
                    }
                )

            cur = con.execute("SELECT value FROM meta WHERE key='next_id'")
            row = cur.fetchone()
            if row is None:
                next_id = 1
            else:
                try:
                    next_id = int(row[0])
                except (TypeError, ValueError):
                    next_id = 1

            return {
                "next_id": next_id,
                "items": items,
            }

    def save_dict(self, data: dict) -> None:
        items = data.get("items") or []
        next_id = data.get("next_id", 1)
        # töröljük a régit
        with self._connect() as con:
            con.execute("DELETE FROM items")
            # újra feltöltjük
            for it in items:
                con.execute(
                    """
                    INSERT INTO items(id, text, priority, done)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        int(it["id"]),
                        str(it["text"]),
                        int(it["priority"]),
                        1 if bool(it["done"]) else 0,  # True:1, False:0
                    ),
                )
            # meta mentése
            con.execute(
                """
                INSERT INTO meta(key, value)
                VALUES('next_id', ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
                """,
                (str(int(next_id)),),
            )
