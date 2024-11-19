from datetime import datetime, timedelta
from app.application.use_cases.task_use_cases import TaskUseCases
from app.infrastructure.repositories.task_repository_impl import (
    TaskRepositoryImpl,
)
from app.application.dtos.task_dto import CreateTaskDTO, UpdateTaskDTO


# Test for Creating a Task
def test_create_task():
    task_use_cases = setup_test()
    # Create the Task
    task_dto = CreateTaskDTO(
        title="Test Task",
        description="This is a test task",
        due_date=datetime.now() + timedelta(days=7),
    )

    created_task = task_use_cases.create_task(task_dto)
    # Assertions
    assert created_task.title == "Test Task"
    assert created_task.description == "This is a test task"
    assert created_task.status == "pending"
    tear_down(created_task.id)


# Test for Updating a Task
def test_update_task():
    task_use_cases = setup_test()
    # Create a Task
    task_dto = CreateTaskDTO(
        title="Test Task",
        description="This is a test task",
        due_date=datetime.now() + timedelta(days=7),
    )

    created_task = task_use_cases.create_task(task_dto)
    # Update the Task
    update_dto = UpdateTaskDTO(
        title="Updated Test Task",
        description="This is an updated test task",
        due_date=created_task.due_date + timedelta(days=3),
    )

    updated_task = task_use_cases.update_task(created_task.id, update_dto)
    # Assertions
    assert updated_task.title == "Updated Test Task"
    assert updated_task.description == "This is an updated test task"
    assert updated_task.due_date == created_task.due_date + timedelta(days=3)
    tear_down(created_task.id)


# Test for Deleting a Task
def test_delete_task():
    task_use_cases = setup_test()
    # Create the Task
    task_dto = CreateTaskDTO(
        title="Test Task",
        description="This is a test task",
        due_date=datetime.now() + timedelta(days=7),
    )

    created_task = task_use_cases.create_task(task_dto)
    # Delete the Tasks
    delete_task = task_use_cases.delete_task(created_task.id)
    # Assertions
    assert delete_task
    tear_down(created_task.id)


# Test for Retrieving a Task
def test_get_task():
    task_use_cases = setup_test()
    # Create the Task
    task_dto = CreateTaskDTO(
        title="Test Task",
        description="This is a test task",
        due_date=datetime.now() + timedelta(days=7),
    )
    created_task = task_use_cases.create_task(task_dto)
    # Retreive the task
    get_task = task_use_cases.get_task(created_task.id)
    # Assertions
    assert get_task.id == created_task.id
    tear_down(created_task.id)


# Helper function for cleaning up tasks
def tear_down(taskid):
    task_repository = TaskRepositoryImpl()
    task_use_cases = TaskUseCases(task_repository)
    print("this is Teardown")
    task_use_cases.delete_task(taskid)


# Helper function setting up task environments
def setup_test():
    task_repository = TaskRepositoryImpl()
    return TaskUseCases(task_repository)
