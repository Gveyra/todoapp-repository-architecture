from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware

from .api_schemas import CreateTodoIn, PriorityIn, TodoOut, ActionResultOut
from .service import TodoApp
from .sqlite_repository import SqliteTodoRepository
from .dto import ListMode

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "todo_table.db"


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.repo = SqliteTodoRepository(str(DB_PATH))
    yield


def get_core(request: Request) -> TodoApp:
    repo = request.app.state.repo
    core = TodoApp(repo)
    core.load()
    return core


app = FastAPI(title="Todo API", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/items", response_model=list[TodoOut])
def list_items(mode: ListMode = ListMode.ALL, core: TodoApp = Depends(get_core)):
    try:
        m = ListMode(mode)
    except Exception:
        raise HTTPException(
            status_code=400, detail="mode must be: all|open|done")
    return core.list_items(m)


@app.post("/items", response_model=ActionResultOut)
def create_item(payload: CreateTodoIn, core: TodoApp = Depends(get_core)):

    try:
        res = core.add(payload.text, payload.priority)

        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/items/{item_id}/toggle", response_model=ActionResultOut)
def toggle_item(item_id: int, core: TodoApp = Depends(get_core)):

    try:
        res = core.toggle_done(item_id)

        return res
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.patch("/items/{item_id}/priority", response_model=ActionResultOut)
def set_priority(item_id: int, payload: PriorityIn, core: TodoApp = Depends(get_core),):

    try:
        res = core.set_priority(item_id, payload.priority)

        return res
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/items/{item_id}", response_model=ActionResultOut)
def delete_item(item_id: int, core: TodoApp = Depends(get_core)):

    try:
        res = core.remove_by_id(item_id)

        return res
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
