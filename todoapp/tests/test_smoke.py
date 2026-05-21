# from .todo.domain import TodoList
# from .storage import MemoryStorage
# from .result_types import AddAction, ToggleAction, PriorityAction, RemoveAction, ListMode


# def run_tests() -> None:
#     app = TodoList(MemoryStorage())

#     r1 = app.add("mosogatás", 2)
#     assert r1["action"] == AddAction.CREATED
#     assert r1["item"]["id"] == 1
#     assert r1["item"]["done"] is False

#     r2 = app.add("  MOSOGATÁS  ", 3)
#     assert r2["action"] == AddAction.MERGED
#     assert r2["item"]["id"] == 1

#     r3 = app.toggle_done(1)
#     assert r3["action"] == ToggleAction.TOGGLED
#     assert r3["item"]["done"] is True

#     r4 = app.set_priority(1, 1)
#     assert r4["action"] == PriorityAction.UPDATED
#     assert r4["item"]["priority"] == 1

#     open_items = app.list_items(ListMode.OPEN)
#     done_items = app.list_items(ListMode.DONE)
#     assert len(open_items) == 0
#     assert len(done_items) == 1

#     r5 = app.remove_by_id(1)
#     assert r5["action"] == RemoveAction.REMOVED
#     assert app.find_by_id(1) is None

#     print("✅ All tests passed!")
