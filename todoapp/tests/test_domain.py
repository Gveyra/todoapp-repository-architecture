import pytest

from todo.domain import TodoList
from todo.dto import (
    AddAction, ToggleAction, PriorityAction, RemoveAction,
    ListMode,
)


def test_add_created_increases_next_id_and_stores_item():
    t = TodoList()

    res = t.add("meditálás", 2)

    assert res["action"] == AddAction.CREATED
    it = res["item"]
    assert it["id"] == 1

    assert it["text"] == "meditálás"
    assert it["priority"] == 2
    assert it["done"] is False
    assert t.next_id == 2
    assert len(t.items) == 1


def test_add_empty_text_raises_value_error():
    t = TodoList()
    with pytest.raises(ValueError):
        t.add("   ", 2)


def test_add_invalid_priority_raises_value_error():
    t = TodoList()
    with pytest.raises(ValueError):
        t.add("alma", 99)
    with pytest.raises(ValueError):
        t.add("alma", "x")


def test_add_same_text_returns_merged_and_does_not_create_new_item():
    t = TodoList()

    r1 = t.add("alma", 2)
    r2 = t.add("alma", 3)

    assert r1["action"] == AddAction.CREATED
    assert r2["action"] == AddAction.MERGED
    assert len(t.items) == 1
    assert t.next_id == 2


def test_toggle_done_flips_boolean():
    t = TodoList()
    t.add("futás", 2)

    r1 = t.toggle_done(1)
    assert r1["action"] == ToggleAction.TOGGLED
    assert r1["item"]["done"] is True

    r2 = t.toggle_done(1)
    assert r2["item"]["done"] is False


def test_toggle_done_missing_id_raises_key_error():
    t = TodoList()
    with pytest.raises(KeyError):
        t.toggle_done(999)


def test_set_priority_updates_priority():
    t = TodoList()
    t.add("tanulás", 2)

    r = t.set_priority(1, 3)
    assert r["action"] == PriorityAction.UPDATED
    assert r["item"]["priority"] == 3


def test_set_priority_invalid_raises_value_error():
    t = TodoList()
    t.add("tanulás", 2)

    with pytest.raises(ValueError):
        t.set_priority(1, 5)


def test_remove_by_id_removes_item():
    t = TodoList()
    t.add("a", 1)
    t.add("b", 2)

    r = t.remove_by_id(1)
    assert r["action"] == RemoveAction.REMOVED
    assert len(t.items) == 1
    assert t.items[0]["id"] == 2


def test_list_items_modes():
    t = TodoList()
    t.add("a", 1)  # id 1 open
    t.add("b", 2)  # id 2 open
    t.toggle_done(2)  # id 2 done

    all_items = t.list_items(ListMode.ALL)
    open_items = t.list_items(ListMode.OPEN)
    done_items = t.list_items(ListMode.DONE)

    assert [it["id"] for it in all_items] == [1, 2]
    assert [it["id"] for it in open_items] == [1]
    assert [it["id"] for it in done_items] == [2]


def test_search_contains_case_insensitive_and_sorted():
    t = TodoList()
    t.add("Alma", 2)
    t.add("banán", 2)
    t.add("almafa", 2)

    res = t.search_contains("ALM")
    assert [it["id"] for it in res] == [1, 3]


def test_from_dict_cleans_invalid_items_and_sets_next_id():
    t = TodoList()

    dirty = {
        "next_id": "x",
        "items": [
            "not a dict",
            {"id": -1, "text": "ok", "priority": 2, "done": False},   # bad id
            {"id": 1, "text": "   ", "priority": 2, "done": False},   # empty text
            # bad priority -> should become 2 (per your cleaning)
            {"id": 2, "text": "ok", "priority": 9, "done": False},
            {"id": 3, "text": "Hello", "priority": 1,
                "done": "yes"},  # done -> bool("yes") True
        ]
    }

    t.from_dict(dirty)

    assert [it["id"] for it in t.items] == [2, 3]
    assert t.items[0]["priority"] == 2
    assert t.items[1]["done"] is True
    assert t.next_id == 4  # max_id=3 -> next_id should be >= 4


def test_invariants_fail_on_duplicate_ids():
    t = TodoList()
    t.items = [
        {"id": 1, "text": "a", "priority": 2, "done": False},
        {"id": 1, "text": "b", "priority": 2, "done": False},
    ]
    t.next_id = 2

    with pytest.raises(RuntimeError):
        t._check_invariants()


def test_sanity():
    assert 1 + 1 == 2
