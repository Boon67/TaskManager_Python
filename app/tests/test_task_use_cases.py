from uuid import uuid4
from datetime import datetime, timedelta
from app.application.use_cases.task_use_cases import TaskUseCases
from app.infrastructure.repositories.task_repository_impl import TaskRepositoryImpl
from app.application.dtos.task_dto import CreateTaskDTO, UpdateTaskDTO


def test_create_task():
    task_repository = TaskRepositoryImpl()
    task_use_cases = TaskUseCases(task_repository)

    task_dto = CreateTaskDTO(
        title="Test Task",
        description="This is a test task",
        due_date=datetime.now() + timedelta(days=7),
    )

    created_task = task_use_cases.create_task(task_dto)

    assert created_task.title == "Test Task"
    assert created_task.description == "This is a test task"
    assert created_task.status == "pending"


def test_update_task():
    task_repository = TaskRepositoryImpl()
    task_use_cases = TaskUseCases(task_repository)

    task_dto = CreateTaskDTO(
        title="Test Task",
        description="This is a test task",
        due_date=datetime.now() + timedelta(days=7),
    )

    created_task = task_use_cases.create_task(task_dto)

    update_dto = UpdateTaskDTO(
        title="Updated Test Task",
        description="This is an updated test task",
        due_date=created_task.due_date + timedelta(days=3),
    )

    updated_task = task_use_cases.update_task(created_task.id, update_dto)

    assert updated_task.title == "Updated Test Task"
    assert updated_task.description == "This is an updated test task"
    assert updated_task.due_date == created_task.due_date + timedelta(days=3)
