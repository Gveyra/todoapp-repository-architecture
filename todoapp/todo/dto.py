from enum import Enum
from typing import TypedDict, Dict, Any

TodoItem = Dict[str, Any]


class AddAction(str, Enum):
    CREATED = "created"
    MERGED = "merged"


class ToggleAction(str, Enum):
    TOGGLED = "toggled"


class PriorityAction(str, Enum):
    UPDATED = "updated"


class RemoveAction(str, Enum):
    REMOVED = "removed"


class ListMode(str, Enum):
    ALL = "all"
    OPEN = "open"
    DONE = "done"


class AddResult(TypedDict):
    action: AddAction
    item: TodoItem


class ToggleResult(TypedDict):
    action: ToggleAction
    item: TodoItem


class PriorityResult(TypedDict):
    action: PriorityAction
    item: TodoItem


class RemoveResult(TypedDict):
    action: RemoveAction
    item: TodoItem
