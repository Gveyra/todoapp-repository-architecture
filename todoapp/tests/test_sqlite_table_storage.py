from todo.sqlite_table_storage import SqliteTableStorage


def test_sqlite_table_storage_roundtrip(tmp_path):
    db_file = tmp_path / "todo_table.db"
    s = SqliteTableStorage(str(db_file))

    original = {
        "next_id": 3,
        "items": [
            {"id": 1, "text": "alma", "priority": 2, "done": False},
            {"id": 2, "text": "banán", "priority": 1, "done": True},
        ],
    }

    s.save_dict(original)
    loaded = s.load_dict()

    assert loaded == original
