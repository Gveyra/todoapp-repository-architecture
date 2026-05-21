from todo.service import TodoApp
from todo.dto import AddAction, ToggleAction, PriorityAction, RemoveAction, ListMode


class FakeTodoRepository:
    def __init__(self):
        self.items = []

    def add(self, item: dict) -> None:
        self.items.append(item.copy())

    def update(self, item: dict) -> None:
        for i, existing in enumerate(self.items):
            if existing["id"] == item["id"]:
                self.items[i] = item.copy()
                return

    def delete(self, item_id: int) -> None:
        self.items = [it for it in self.items if it["id"] != item_id]

    def get_by_id(self, item_id: int) -> dict | None:
        for it in self.items:
            if it["id"] == item_id:
                return it.copy()
        return None

    def list_all(self) -> list[dict]:
        return [it.copy() for it in self.items]


def test_add_saves_created_item_to_repo():
    repo = FakeTodoRepository()
    app = TodoApp(repo)
    app.load()

    result = app.add("Tanulás", 1)

    assert result["action"] == AddAction.CREATED
    assert repo.list_all() == [
        {"id": 1, "text": "tanulás", "priority": 1, "done": False}
    ]


def test_list_items_loads_from_repo():
    repo = FakeTodoRepository()
    repo.add({"id": 1, "text": "python", "priority": 2, "done": False})

    app = TodoApp(repo)
    app.load()

    assert app.list_items(ListMode.ALL) == [
        {"id": 1, "text": "python", "priority": 2, "done": False}
    ]


def test_toggle_updates_repo():
    repo = FakeTodoRepository()
    repo.add({"id": 1, "text": "python", "priority": 2, "done": False})

    app = TodoApp(repo)
    app.load()

    result = app.toggle_done(1)

    assert result["action"] == ToggleAction.TOGGLED
    assert repo.get_by_id(1)["done"] is True


def test_set_priority_updates_repo():
    repo = FakeTodoRepository()
    repo.add({"id": 1, "text": "python", "priority": 2, "done": False})

    app = TodoApp(repo)
    app.load()

    result = app.set_priority(1, 3)

    assert result["action"] == PriorityAction.UPDATED
    assert repo.get_by_id(1)["priority"] == 3


def test_remove_deletes_from_repo():
    repo = FakeTodoRepository()
    repo.add({"id": 1, "text": "python", "priority": 2, "done": False})

    app = TodoApp(repo)
    app.load()

    result = app.remove_by_id(1)

    assert result["action"] == RemoveAction.REMOVED
    assert repo.list_all() == []
