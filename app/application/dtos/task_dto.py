from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class CreateTaskDTO(BaseModel):
    title: str
    description: str
    due_date: datetime


class UpdateTaskDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskResponseDTO(BaseModel):
    id: UUID
    title: str
    description: str
    due_date: datetime
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
