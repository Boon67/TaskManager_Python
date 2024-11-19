# app/infrastructure/repositories/task_repository_impl.py
from typing import List, Optional
from uuid import UUID
from ...domain.interfaces.task_repository import TaskRepository
from ...domain.entities.task import Task
from ..database import SessionLocal, Base, engine
from sqlalchemy import Column, String, DateTime, Table

# SQLAlchemy model
tasks_table = Table(
    "tasks",
    Base.metadata,
    Column("id", String, primary_key=True),
    Column("title", String),
    Column("description", String),
    Column("due_date", DateTime),
    Column("status", String),
    Column("created_at", DateTime),
    Column("updated_at", DateTime, nullable=True),
)


class TaskRepositoryImpl(TaskRepository):
    def __init__(self):
        Base.metadata.create_all(bind=engine)

    def _get_db(self):
        db = SessionLocal()
        try:
            return db
        finally:
            db.close()

    def create(self, task: Task) -> Task:
        """Creates a task based upon the task object

        Args:
            task (Task): Task Object

        Returns:
            Task: Task Object
        """
        db = self._get_db()
        db_task = dict(
            id=str(task.id),
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            status=task.status,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
        db.execute(tasks_table.insert().values(**db_task))
        db.commit()
        return task

    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        """Retrieves a task by the ID

        Args:
            task_id (UUID): UUID of the reference tasks

        Returns:
            Optional[Task]: Returns a task object if found
        """
        db = self._get_db()
        result = db.execute(
            tasks_table.select().where(tasks_table.c.id == str(task_id))
        ).first()
        if result:
            return Task(
                id=UUID(result.id),
                title=result.title,
                description=result.description,
                due_date=result.due_date,
                status=result.status,
                created_at=result.created_at,
                updated_at=result.updated_at,
            )
        return None

    def get_all(self) -> List[Task]:
        """Retrieves all the tasks from the repository

        Returns:
            List[Task]: Dictionary of Task objects
        """
        db = self._get_db()
        results = db.execute(tasks_table.select()).fetchall()
        return [
            Task(
                id=UUID(result.id),
                title=result.title,
                description=result.description,
                due_date=result.due_date,
                status=result.status,
                created_at=result.created_at,
                updated_at=result.updated_at,
            )
            for result in results
        ]

    def update(self, task: Task) -> Task:
        """Updates a task based upon the task object passed

        Args:
            task (Task): Task Object

        Returns:
            Task: Returns the updated task.
        """
        db = self._get_db()
        db_task = dict(
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            status=task.status,
            updated_at=task.updated_at,
        )
        db.execute(
            tasks_table.update()
            .where(tasks_table.c.id == str(task.id))
            .values(**db_task)
        )
        db.commit()
        return task

    def delete(self, task_id: UUID) -> bool:
        """Deletes a given task based upon the UUID

        Args:
            task_id (UUID): UUID of the task to be deleted

        Returns:
            bool: Returns True if successful
        """
        db = self._get_db()
        result = db.execute(
            tasks_table.delete().where(tasks_table.c.id == str(task_id))
        )
        db.commit()
        return result.rowcount > 0
