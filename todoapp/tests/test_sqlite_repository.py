from todo.sqlite_repository import SqliteTodoRepository


def test_add_and_list_all(tmp_path):
    db_path = tmp_path / "test.db"
    repo = SqliteTodoRepository(str(db_path))

    item = {
        "id": 1,
        "text": "Learn repository",
        "priority": 2,
        "done": False,
    }

    repo.add(item)

    assert repo.list_all() == [item]


def test_update_item(tmp_path):
    db_path = tmp_path / "test.db"
    repo = SqliteTodoRepository(str(db_path))

    item = {
        "id": 1,
        "text": "Old text",
        "priority": 2,
        "done": False,
    }

    repo.add(item)

    updated = {
        "id": 1,
        "text": "New text",
        "priority": 1,
        "done": True,
    }

    repo.update(updated)

    assert repo.get_by_id(1) == updated


def test_delete_item(tmp_path):
    db_path = tmp_path / "test.db"
    repo = SqliteTodoRepository(str(db_path))

    item = {
        "id": 1,
        "text": "Delete me",
        "priority": 2,
        "done": False,
    }

    repo.add(item)
    repo.delete(1)

    assert repo.get_by_id(1) is None
    assert repo.list_all() == []
