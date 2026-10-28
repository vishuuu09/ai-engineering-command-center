
import json
import sqlite3
from pathlib import Path
from typing import Any

DATABASE_PATH = Path(__file__).resolve().parent.parent / "command_center.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                requirement TEXT NOT NULL,
                total_estimated_hours REAL NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                task_code TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                priority TEXT NOT NULL,
                estimated_hours REAL NOT NULL,
                dependencies TEXT NOT NULL DEFAULT '[]',
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id)
                    REFERENCES projects(id)
                    ON DELETE CASCADE,
                UNIQUE(project_id, task_code)
            );

            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                project_name TEXT NOT NULL,
                task_code TEXT,
                task_title TEXT,
                activity_type TEXT NOT NULL,
                description TEXT NOT NULL,
                old_status TEXT,
                new_status TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id)
                    REFERENCES projects(id)
                    ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_activities_created_at
            ON activities(created_at DESC);
            """
        )


def save_task_breakdown(
    project_name: str,
    requirement: str,
    tasks: list[Any],
) -> int:
    total_hours = sum(float(task.estimated_hours) for task in tasks)

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO projects (
                project_name,
                requirement,
                total_estimated_hours
            )
            VALUES (?, ?, ?)
            """,
            (project_name, requirement, total_hours),
        )
        project_id = int(cursor.lastrowid)

        for task in tasks:
            connection.execute(
                """
                INSERT INTO tasks (
                    project_id,
                    task_code,
                    title,
                    description,
                    priority,
                    estimated_hours,
                    dependencies,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    project_id,
                    task.id,
                    task.title,
                    task.description,
                    task.priority,
                    task.estimated_hours,
                    json.dumps(task.dependencies),
                    task.status,
                ),
            )

        connection.execute(
            """
            INSERT INTO activities (
                project_id,
                project_name,
                activity_type,
                description
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                project_id,
                project_name,
                "project_created",
                f"Project '{project_name}' was created with {len(tasks)} tasks.",
            ),
        )

    return project_id


def get_saved_projects() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, project_name, requirement,
                   total_estimated_hours, created_at
            FROM projects
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def get_saved_tasks(project_id: int) -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT task_code, title, description, priority,
                   estimated_hours, dependencies, status, created_at
            FROM tasks
            WHERE project_id = ?
            ORDER BY id
            """,
            (project_id,),
        ).fetchall()

    tasks = []
    for row in rows:
        task = dict(row)
        task["dependencies"] = json.loads(task["dependencies"])
        tasks.append(task)

    return tasks


def update_saved_task_status(
    project_id: int,
    task_code: str,
    status: str,
) -> bool:
    if status not in {"Pending", "In Progress", "Done"}:
        raise ValueError("Invalid task status")

    with get_connection() as connection:
        task = connection.execute(
            """
            SELECT t.title, t.status, p.project_name
            FROM tasks AS t
            JOIN projects AS p ON p.id = t.project_id
            WHERE t.project_id = ? AND t.task_code = ?
            """,
            (project_id, task_code),
        ).fetchone()

        if task is None:
            return False

        old_status = task["status"]

        # Don't create duplicate activity when the status hasn't changed.
        if old_status == status:
            return True

        connection.execute(
            """
            UPDATE tasks
            SET status = ?
            WHERE project_id = ? AND task_code = ?
            """,
            (status, project_id, task_code),
        )

        connection.execute(
            """
            INSERT INTO activities (
                project_id,
                project_name,
                task_code,
                task_title,
                activity_type,
                description,
                old_status,
                new_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                project_id,
                task["project_name"],
                task_code,
                task["title"],
                "task_status_changed",
                (
                    f"{task_code} ({task['title']}) changed "
                    f"from {old_status} to {status}."
                ),
                old_status,
                status,
            ),
        )

    return True


def get_recent_activities(limit: int = 50) -> list[dict]:
    limit = max(1, min(int(limit), 200))

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, project_id, project_name,
                   task_code, task_title, activity_type,
                   description, old_status, new_status, created_at
            FROM activities
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


initialize_database()
