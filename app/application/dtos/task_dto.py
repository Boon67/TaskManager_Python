# app/domain/entities/task.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class CreateTaskDTO(BaseModel):
    """
    DTO for Creating Task Information
    Args:
        BaseModel (_type_): _description_
    """

    title: str
    description: str
    due_date: datetime


class UpdateTaskDTO(BaseModel):
    """DTO for Updating Tasks where not all the properties may be set

    Args:
        BaseModel (_type_): _description_
    """

    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskResponseDTO(BaseModel):
    """DTO for Response from the Operation. Which contains the full task

    Args:
        BaseModel (_type_): _description_
    """

    id: UUID
    title: str
    description: str
    due_date: datetime
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
