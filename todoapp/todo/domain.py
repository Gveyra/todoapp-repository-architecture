from typing import Optional, List
from .dto import (TodoItem,
                  AddResult, ToggleResult, PriorityResult, RemoveResult,
                  AddAction, ToggleAction, PriorityAction, RemoveAction, ListMode
                  )


class TodoList:
    def __init__(self) -> None:
        self.items: List[TodoItem] = []
        self.next_id: int = 1


# ---------------helpers-----------------------

    def _norm_text(self, text: str) -> str:
        return str(text).strip().lower()

    def _require_item(self, item_id: int) -> TodoItem:
        it = self.find_by_id(item_id)
        if not it:
            raise KeyError("Nincs ilyen ID")
        return it

    def _validate_text(self, text: str) -> str:
        t = self._norm_text(text)
        if not t:
            raise ValueError("A feladat szövege nem lehet üres")
        return t

    def _validate_priority(self, prio: int) -> int:
        try:
            p = int(prio)
        except (TypeError, ValueError):
            raise ValueError("A prioritásnak számnak kell lennie (1-3)")
        if p not in (1, 2, 3):
            raise ValueError("A prioritás csak 1,2 vagy 3 lehet")
        return p

    # ---------- query ----------

    def find_by_id(self, item_id: int) -> Optional[TodoItem]:
        for it in self.items:
            if it["id"] == item_id:
                return it
        return None

    def find_by_text_exact(self, text: str) -> Optional[TodoItem]:
        t = self._norm_text(text)
        if not t:
            return None
        for it in self.items:
            if self._norm_text(it.get("text", "")) == t:
                return it
        return None

    def search_contains(self, query: str) -> List[TodoItem]:
        q = self._norm_text(query)
        if not q:
            return []
        res = [it for it in self.items if q in self._norm_text(
            it.get("text", ""))]
        return sorted(res, key=lambda it: it["id"])

    def list_items(self, mode: ListMode = ListMode.ALL) -> List[TodoItem]:
        if mode == ListMode.ALL:
            res = list(self.items)
        elif mode == ListMode.OPEN:
            res = [it for it in self.items if not it.get("done", False)]
        else:  # DONE
            res = [it for it in self.items if it.get("done", False)]
        return sorted(res, key=lambda it: it["id"])

        # ---------- mutations ----------
    def _create_item(self, text: str, priority: int) -> TodoItem:
        it = {"id": self.next_id, "text": text,
              "priority": priority, "done": False}
        self.items.append(it)
        self.next_id += 1
        return it

    def add(self, text: str, priority: int = 2) -> AddResult:
        t = self._validate_text(text)
        p = self._validate_priority(priority)

        existing = self.find_by_text_exact(t)
        if existing:
            return {"action": AddAction.MERGED, "item": existing}

        created = self._create_item(t, p)
        self._check_invariants()
        return {"action": AddAction.CREATED, "item": created}

    def toggle_done(self, item_id: int) -> ToggleResult:
        it = self._require_item(item_id)

        it["done"] = not bool(it.get("done", False))
        self._check_invariants()
        return {"action": ToggleAction.TOGGLED, "item": it}

    def set_priority(self, item_id: int, priority: int) -> PriorityResult:
        it = self._require_item(item_id)
        p = self._validate_priority(priority)
        it["priority"] = p
        self._check_invariants()
        return {"action": PriorityAction.UPDATED, "item": it}

    def remove_by_id(self, item_id: int) -> RemoveResult:
        it = self._require_item(item_id)
        self.items.remove(it)
        self._check_invariants()
        return {"action": RemoveAction.REMOVED, "item": it}

     # ---------- persistence mapping ----------

    def to_dict(self) -> dict:
        return {"next_id": self.next_id, "items": self.items}

    def from_dict(self, data: dict) -> None:
        loaded_items = data.get("items") or []
        loaded_next_id = data.get("next_id", 1)

        cleaned: List[TodoItem] = []
        if isinstance(loaded_items, list):
            for raw in loaded_items:
                if not isinstance(raw, dict):
                    continue

                text = raw.get("text")
                t = self._norm_text(text) if text is not None else ""
                if not t:
                    continue

                try:
                    i_id = int(raw.get("id", 0))

                    prio = int(raw.get("priority", 2))
                    done = bool(raw.get("done", False))
                except (TypeError, ValueError):
                    continue

                if i_id <= 0:
                    continue
                if prio not in (1, 2, 3):
                    prio = 2

                cleaned.append(
                    {"id": i_id, "text": t, "priority": prio, "done": done})
        self.items = cleaned

        max_id = max((it["id"] for it in self.items), default=0)
        try:
            loaded_next_id = int(loaded_next_id)
        except (TypeError, ValueError):
            loaded_next_id = max_id + 1
        self.next_id = max(loaded_next_id, max_id + 1)
        self._check_invariants()

# ---------------invariats-------------

    def _check_invariants(self) -> None:
        # 1) items list?
        if not isinstance(self.items, list):
            raise RuntimeError("Invariant broken: items is not a list")

        ids: list[int] = []

        for it in self.items:
            # 2) minden elem dict?
            if not isinstance(it, dict):
                raise RuntimeError("Invariant broken: item is not a dict")

        # 3) id: pozitív int
            try:
                i_id = int(it.get("id"))
            except (TypeError, ValueError):
                raise RuntimeError("Invariant broken: invalid id")

            if i_id <= 0:
                raise RuntimeError("Invariant broken: id must be positive")

            ids.append(i_id)

        # 4) priority:1..3
            try:
                p = int(it.get("priority", 2))
            except (TypeError, ValueError):
                raise RuntimeError("Invariant broken: priority must be int")

            if p not in (1, 2, 3):
                raise RuntimeError("Invariant broken: priority must be 1..3")
        # 5) done: bool
            if not isinstance(it.get("done", False), bool):
                raise RuntimeError("Invariant broken: done must be bool")
        # 6) text: nem üres (nem normalizáció, csak üresség! )
            text = it.get("text")
            if not isinstance(text, str) or text.strip() == "":
                raise RuntimeError("Invariant broken: text cannot be empty")
    # 7) ID egyedi
        if len(ids) != len(set(ids)):
            raise RuntimeError("Invariant broken: duplicated IDs detected")
    # 8) next_id konzisztens
        try:
            nid = int(self.next_id)
        except (TypeError, ValueError):
            raise RuntimeError("Invariant broken: next_id must be int")
        max_id = max(ids, default=0)
        if nid <= max_id:
            raise RuntimeError("Invariant broken: next_id must be > max_id")
