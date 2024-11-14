# app/domain/entities/task.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

"""Domain model for the Task Object
"""


@dataclass
class Task:
    title: str
    description: str
    due_date: datetime
    status: str
    id: UUID = uuid4()
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None

    def mark_as_complete(self):
        self.status = "completed"
        self.updated_at = datetime.now()

    def update(
        self, title: str = None, description: str = None, due_date: datetime = None
    ):
        if title:
            self.title = title
        if description:
            self.description = description
        if due_date:
            self.due_date = due_date
        self.updated_at = datetime.now()
