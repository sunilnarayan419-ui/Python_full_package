"""A persistent, professional to-do list application.

Layers: Task (model) -> TaskRepository (JSON persistence) ->
TaskService (business rules) -> CLI (presentation).
"""

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from enum import Enum
from pathlib import Path

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_STORAGE_PATH = Path.cwd() / "data" / "todo_list.json"


class TaskError(Exception):
    """Base exception for task-related failures."""


class TaskNotFoundError(TaskError):
    """Raised when a requested task ID does not exist."""


class InvalidTaskDataError(TaskError):
    """Raised when task input data fails validation."""


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"


@dataclass(slots=True)
class Task:
    """Represents a single to-do item."""

    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    due_date: str | None = None
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def to_dict(self) -> dict:
        data = asdict(self)
        data["priority"] = self.priority.value
        data["status"] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            priority=Priority(data.get("priority", "medium")),
            status=Status(data.get("status", "pending")),
            due_date=data.get("due_date"),
            created_at=data.get("created_at", datetime.now().isoformat(timespec="seconds")),
        )


class TaskRepository:
    """Handles JSON persistence for tasks."""

    def __init__(self, storage_path: Path = DEFAULT_STORAGE_PATH) -> None:
        self._storage_path = storage_path
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._storage_path.exists():
            self._write_all([])

    def load_all(self) -> list[Task]:
        try:
            raw = self._storage_path.read_text(encoding="utf-8")
            payload = json.loads(raw) if raw.strip() else []
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load tasks (%s); starting with empty list.", exc)
            return []
        return [Task.from_dict(item) for item in payload]

    def save_all(self, tasks: list[Task]) -> None:
        self._write_all([task.to_dict() for task in tasks])

    def _write_all(self, payload: list[dict]) -> None:
        tmp_path = self._storage_path.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        tmp_path.replace(self._storage_path)


class TaskService:
    """Business logic for managing tasks, independent of any UI."""

    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository
        self._tasks: dict[str, Task] = {t.id: t for t in repository.load_all()}

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        due_date: str | None = None,
    ) -> Task:
        if not title.strip():
            raise InvalidTaskDataError("Task title cannot be empty.")
        if due_date is not None:
            self._validate_date(due_date)

        task = Task(title=title.strip(), description=description.strip(),
                     priority=priority, due_date=due_date)
        self._tasks[task.id] = task
        self._persist()
        return task

    def update_task(self, task_id: str, **fields) -> Task:
        task = self._get_or_raise(task_id)
        if "title" in fields and fields["title"] is not None:
            title = fields["title"].strip()
            if not title:
                raise InvalidTaskDataError("Task title cannot be empty.")
            task.title = title
        if "description" in fields and fields["description"] is not None:
            task.description = fields["description"].strip()
        if "priority" in fields and fields["priority"] is not None:
            task.priority = fields["priority"]
        if "due_date" in fields and fields["due_date"] is not None:
            self._validate_date(fields["due_date"])
            task.due_date = fields["due_date"]
        self._persist()
        return task

    def mark_completed(self, task_id: str) -> Task:
        task = self._get_or_raise(task_id)
        task.status = Status.COMPLETED
        self._persist()
        return task

    def delete_task(self, task_id: str) -> None:
        self._get_or_raise(task_id)
        del self._tasks[task_id]
        self._persist()

    def list_tasks(
        self,
        status: Status | None = None,
        priority: Priority | None = None,
        sort_by_due_date: bool = False,
    ) -> list[Task]:
        tasks = list(self._tasks.values())
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        if priority is not None:
            tasks = [t for t in tasks if t.priority == priority]
        if sort_by_due_date:
            tasks.sort(key=lambda t: (t.due_date is None, t.due_date or ""))
        else:
            tasks.sort(key=lambda t: t.created_at)
        return tasks

    def _get_or_raise(self, task_id: str) -> Task:
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"No task found with ID '{task_id}'.")
        return task

    @staticmethod
    def _validate_date(value: str) -> None:
        try:
            date.fromisoformat(value)
        except ValueError as exc:
            raise InvalidTaskDataError(
                f"Invalid due date '{value}'. Use YYYY-MM-DD format."
            ) from exc

    def _persist(self) -> None:
        self._repository.save_all(list(self._tasks.values()))


def _print_menu() -> None:
    print("\n================================")
    print("          TO-DO LIST")
    print("================================")
    print("1. Add task")
    print("2. List tasks")
    print("3. Update task")
    print("4. Mark task completed")
    print("5. Delete task")
    print("0. Exit")


def _print_task(task: Task) -> None:
    due = task.due_date or "none"
    print(f"[{task.id}] {task.title} | priority={task.priority.value} "
          f"| status={task.status.value} | due={due}")


def _handle_add(service: TaskService) -> None:
    title = input("Title: ").strip()
    description = input("Description (optional): ").strip()
    priority_raw = input("Priority (low/medium/high) [medium]: ").strip().lower() or "medium"
    due_date = input("Due date YYYY-MM-DD (optional): ").strip() or None
    try:
        priority = Priority(priority_raw)
        task = service.add_task(title, description, priority, due_date)
        print(f"Added task {task.id}.")
    except (ValueError, TaskError) as exc:
        print(f"Error: {exc}")


def _handle_list(service: TaskService) -> None:
    tasks = service.list_tasks(sort_by_due_date=True)
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        _print_task(task)


def _handle_update(service: TaskService) -> None:
    task_id = input("Task ID: ").strip()
    title = input("New title (leave blank to keep): ").strip() or None
    description = input("New description (leave blank to keep): ").strip() or None
    due_date = input("New due date YYYY-MM-DD (leave blank to keep): ").strip() or None
    try:
        task = service.update_task(task_id, title=title, description=description, due_date=due_date)
        print(f"Updated task {task.id}.")
    except TaskError as exc:
        print(f"Error: {exc}")


def _handle_complete(service: TaskService) -> None:
    task_id = input("Task ID: ").strip()
    try:
        service.mark_completed(task_id)
        print("Task marked completed.")
    except TaskError as exc:
        print(f"Error: {exc}")


def _handle_delete(service: TaskService) -> None:
    task_id = input("Task ID: ").strip()
    try:
        service.delete_task(task_id)
        print("Task deleted.")
    except TaskError as exc:
        print(f"Error: {exc}")


def main() -> None:
    """Entry point for the interactive to-do list CLI."""
    service = TaskService(TaskRepository())
    actions = {
        "1": _handle_add,
        "2": _handle_list,
        "3": _handle_update,
        "4": _handle_complete,
        "5": _handle_delete,
    }

    while True:
        _print_menu()
        choice = input("Select an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid choice.")
            continue
        action(service)


if __name__ == "__main__":
    main()
