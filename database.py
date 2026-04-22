import sqlite3
from dataclasses import dataclass
from typing import Optional


database_name = "tasks.db"

@dataclass
class Task:
    name: str
    important: bool
    immediately: bool
    done: bool = False
    id: Optional[int] = None


class TaskDatabase:
    def __init__(self, db_name: str = database_name) -> None:
        self.db_name = db_name
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_name)

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    important INTEGER NOT NULL CHECK (important IN (0, 1)),
                    immediately INTEGER NOT NULL CHECK (immediately IN (0, 1)),
                    done INTEGER NOT NULL CHECK (done IN (0, 1)))
                """)

    def add_task(self, task: Task) -> None:
        query = """
            INSERT INTO tasks (name, important, immediately, done)
            VALUES (?, ?, ?, ?)
            """

        with self._get_connection() as conn:
            conn.execute(query, (
                task.name,
                int(task.important),
                int(task.immediately),
                int(task.done)
            ))

    def delete_task(self, task_id: int) -> None:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    def update_task(self, task: Task) -> None:
        if task.id is None:
            return

        query = """
            UPDATE tasks 
            SET name = ?, important = ?, immediately = ?, done = ?
            WHERE id = ?
        """
        with self._get_connection() as conn:
            conn.execute(query, (
                task.name,
                int(task.important),
                int(task.immediately),
                int(task.done),
                task.id
            ))

    def get_all_tasks(self) -> list[Task]:
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM tasks").fetchall()

            return [Task(
                id=row["id"],
                name=row["name"],
                important=bool(row["important"]),
                immediately=bool(row["immediately"]),
                done=bool(row["done"])
            ) for row in rows]



