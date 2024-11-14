# app/domain/interfaces/task_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ..entities.task import Task

"""Interface defnition for the required operations
"""


class TaskRepository(ABC):
    """Defines the ABC for Interfaces
    to be implemented on the repository

    Args:
        ABC (_type_): Abstract Base Class
    """

    @abstractmethod
    def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        pass

    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        pass

    @abstractmethod
    def delete(self, task_id: UUID) -> bool:
        pass
