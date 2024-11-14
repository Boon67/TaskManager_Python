# app/application/use_cases/task_use_cases.py
from typing import List
from uuid import UUID, uuid4
from ...domain.interfaces.task_repository import TaskRepository
from ...domain.entities.task import Task
from ..dtos.task_dto import CreateTaskDTO, UpdateTaskDTO, TaskResponseDTO


class TaskUseCases:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def create_task(self, task_dto: CreateTaskDTO) -> TaskResponseDTO:
        """Creates a task  of type CreateTaskDTO

        Args:
            task_dto (CreateTaskDTO): CreateTaskDTO Object

        Returns:
            TaskResponseDTO: Returns the full task object response
        """
        task = Task(
            id=uuid4(),
            title=task_dto.title,
            description=task_dto.description,
            due_date=task_dto.due_date,
            status="pending",
        )
        created_task = self.task_repository.create(task)
        return TaskResponseDTO.model_validate(created_task.__dict__)

    def get_task(self, task_id: UUID) -> TaskResponseDTO:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        return TaskResponseDTO.model_validate(task.__dict__)

    def get_all_tasks(self) -> List[TaskResponseDTO]:
        tasks = self.task_repository.get_all()
        return [TaskResponseDTO.model_validate(task.__dict__) for task in tasks]

    def update_task(self, task_id: UUID, task_dto: UpdateTaskDTO) -> TaskResponseDTO:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")

        task.update(
            title=task_dto.title,
            description=task_dto.description,
            due_date=task_dto.due_date,
        )
        updated_task = self.task_repository.update(task)
        return TaskResponseDTO.model_validate(updated_task.__dict__)

    def complete_task(self, task_id: UUID) -> TaskResponseDTO:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")

        task.mark_as_complete()
        updated_task = self.task_repository.update(task)
        return TaskResponseDTO.model_validate(updated_task.__dict__)

    def delete_task(self, task_id: UUID) -> bool:
        return self.task_repository.delete(task_id)
