import sqlite3


class SqliteTodoRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _ensure_table(self) -> None:
        with self._connect() as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY,
                    text TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    done INTEGER NOT NULL
                )
            """)

    def add(self, item: dict) -> None:
        with self._connect() as con:
            con.execute(
                "INSERT INTO items (id, text, priority, done) VALUES (?, ?, ?, ?)",
                (item["id"], item["text"], item["priority"], int(item["done"]))
            )

    def update(self, item: dict) -> None:
        with self._connect() as con:
            con.execute(
                "UPDATE items SET text = ?, priority = ?, done = ? WHERE id = ?",
                (item["text"], item["priority"], int(item["done"]), item["id"])
            )

    def delete(self, item_id: int) -> None:
        with self._connect() as con:
            con.execute(
                "DELETE FROM items WHERE id = ?",
                (item_id,)
            )

    def get_by_id(self, item_id: int) -> dict | None:
        with self._connect() as con:
            row = con.execute(
                "SELECT id, text, priority, done FROM items WHERE id = ?",
                (item_id,)
            ).fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "text": row[1],
            "priority": row[2],
            "done": bool(row[3]),
        }

    def list_all(self) -> list[dict]:
        with self._connect() as con:
            rows = con.execute(
                "SELECT id, text, priority, done FROM items ORDER BY id"
            ).fetchall()

        return [
            {
                "id": row[0],
                "text": row[1],
                "priority": row[2],
                "done": bool(row[3]),
            }
            for row in rows
        ]
