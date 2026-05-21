from fastapi.testclient import TestClient

from todo.api import app, get_core
from todo.service import TodoApp
from todo.sqlite_repository import SqliteTodoRepository


def test_api_crud_flow(tmp_path):
    db_path = tmp_path / "test_api.db"
    repo = SqliteTodoRepository(str(db_path))

    def override_get_core():
        core = TodoApp(repo)
        core.load()
        return core

    app.dependency_overrides[get_core] = override_get_core

    client = TestClient(app)

    response = client.post(
        "/items",
        json={"text": "Tanulás", "priority": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["item"]["text"] == "tanulás"
    assert data["item"]["priority"] == 1
    item_id = data["item"]["id"]

    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.post(f"/items/{item_id}/toggle")
    assert response.status_code == 200
    assert response.json()["item"]["done"] is True

    response = client.patch(
        f"/items/{item_id}/priority",
        json={"priority": 3},
    )
    assert response.status_code == 200
    assert response.json()["item"]["priority"] == 3

    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200

    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()
