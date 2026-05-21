from pydantic import BaseModel, Field


class CreateTodoIn(BaseModel):
    text: str
    priority: int = Field(default=2, ge=1, le=3)


class PriorityIn(BaseModel):
    priority: int = Field(ge=1, le=3)


class TodoOut(BaseModel):
    id: int
    text: str
    priority: int
    done: bool


class ActionResultOut(BaseModel):
    action: str
    item: TodoOut
