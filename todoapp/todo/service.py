from dataclasses import dataclass, field
from .domain import TodoList
from .repository import TodoRepository
from .dto import ListMode


@dataclass
class TodoApp:
    repo: TodoRepository
    domain: TodoList = field(default_factory=TodoList)


# --------------persistence---------------


    def load(self) -> None:
        items = self.repo.list_all()
        self.domain.items = items
        self.domain.next_id = self._calc_next_id(items)

    def _calc_next_id(self, items: list[dict]) -> int:
        if not items:
            return 1
        return max(item["id"] for item in items) + 1

    def list_items(self, mode: ListMode = ListMode.ALL):
        return self.domain.list_items(mode)

    def search_contains(self, query: str):
        return self.domain.search_contains(query)

    def find_by_id(self, item_id: int):
        return self.domain.find_by_id(item_id)

    def remove(self, item_id: int):
        return self.remove_by_id(item_id)

# -------------- use cases ---------------

    def add(self, text: str, priority: int = 2):
        result = self.domain.add(text, priority)

        item = result["item"]

        # csak CREATED esetén INSERT
        if result["action"].value == "created":
            self.repo.add(item)
        return result

    def toggle_done(self, item_id: int):
        result = self.domain.toggle_done(item_id)

        item = result["item"]
        self.repo.update(item)

        return result

    def set_priority(self, item_id: int, priority: int):
        result = self.domain.set_priority(item_id, priority)

        item = result["item"]
        self.repo.update(item)

        return result

    def remove_by_id(self, item_id: int):
        result = self.domain.remove_by_id(item_id)

        self.repo.delete(item_id)

        return result
