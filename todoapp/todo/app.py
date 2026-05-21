from pathlib import Path

from .sqlite_repository import SqliteTodoRepository
from .service import TodoApp
from .cli import TodoCLI

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "todo_table.db"


def main() -> None:
    repo = SqliteTodoRepository(str(DB_PATH))
    core = TodoApp(repo)
    core.load()
    TodoCLI(core).run()


if __name__ == "__main__":
    main()
