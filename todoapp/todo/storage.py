# Alternative / test-oriented storages:
# - MemoryStorage: tests
# - JsonStorage: simple file persistence
# Main production-like storage currently: sqlite_table_storage.py

import json
from pathlib import Path
from typing import Optional


class Storage:
    def load_dict(self) -> dict:  # interface / szerződés
        raise NotImplementedError

    def save_dict(self, data: dict) -> None:  # interface / szerződés
        raise NotImplementedError


class JsonStorage:
    def __init__(self, filename: str = "items.json"):
        self.path = Path(__file__).with_name(filename)

    def load_dict(self) -> dict:
        if not self.path.exists():
            return {}
        raw = self.path.read_text(encoding="utf-8").strip()
        if raw == "":
            return {}
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}

    def save_dict(self, data: dict) -> None:
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                             encoding="utf-8"
                             )


class MemoryStorage(JsonStorage):
    def __init__(self, initial: Optional[dict] = None):
        self._data = initial or {}

    def load_dict(self) -> dict:
        return dict(self._data)

    def save_dict(self, data: dict) -> None:
        self._data = dict(data)
