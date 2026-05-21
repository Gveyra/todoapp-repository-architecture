
from todo.sqlite_storage import SqliteStorage


def test_sqlite_storage_roundtrip(tmp_path):
    # tmp_path alá rakjuk a db-t
    db_file = tmp_path / "todo.db"
    s = SqliteStorage(str(db_file))

    original = {"next_id": 3, "items": [
        {"id": 1, "text": "a", "priority": 2, "done": False}]}
    s.save_dict(original)

    data = s.load_dict()
    assert data == original
