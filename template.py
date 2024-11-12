# Directory structure:
# /app
#   /domain
#     /entities
#       task.py
#     /interfaces
#       task_repository.py
#   /infrastructure
#     /repositories
#       task_repository_impl.py
#     database.py
#   /application
#     /use_cases
#       task_use_cases.py
#     /dtos
#       task_dto.py
#   /presentation
#     /controllers
#       task_controller.py
#   main.py
#   config.py

# app/domain/entities/task.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

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

    def update(self, title: str = None, description: str = None, due_date: datetime = None):
        if title:
            self.title = title
        if description:
            self.description = description
        if due_date:
            self.due_date = due_date
        self.updated_at = datetime.now()

# app/domain/interfaces/task_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ..entities.task import Task

class TaskRepository(ABC):
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

# app/infrastructure/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# app/infrastructure/repositories/task_repository_impl.py
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from ...domain.interfaces.task_repository import TaskRepository
from ...domain.entities.task import Task
from ..database import SessionLocal, Base, engine
from sqlalchemy import Column, String, DateTime, Table

# SQLAlchemy model
tasks_table = Table(
    'tasks',
    Base.metadata,
    Column('id', String, primary_key=True),
    Column('title', String),
    Column('description', String),
    Column('due_date', DateTime),
    Column('status', String),
    Column('created_at', DateTime),
    Column('updated_at', DateTime, nullable=True)
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
        db = self._get_db()
        db_task = dict(
            id=str(task.id),
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            status=task.status,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        db.execute(tasks_table.insert().values(**db_task))
        db.commit()
        return task

    def get_by_id(self, task_id: UUID) -> Optional[Task]:
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
                updated_at=result.updated_at
            )
        return None

    def get_all(self) -> List[Task]:
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
                updated_at=result.updated_at
            )
            for result in results
        ]

    def update(self, task: Task) -> Task:
        db = self._get_db()
        db_task = dict(
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            status=task.status,
            updated_at=task.updated_at
        )
        db.execute(
            tasks_table.update()
            .where(tasks_table.c.id == str(task.id))
            .values(**db_task)
        )
        db.commit()
        return task

    def delete(self, task_id: UUID) -> bool:
        db = self._get_db()
        result = db.execute(
            tasks_table.delete().where(tasks_table.c.id == str(task_id))
        )
        db.commit()
        return result.rowcount > 0

# app/application/dtos/task_dto.py
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

# app/application/use_cases/task_use_cases.py
from typing import List
from uuid import UUID
from ...domain.interfaces.task_repository import TaskRepository
from ...domain.entities.task import Task
from ..dtos.task_dto import CreateTaskDTO, UpdateTaskDTO, TaskResponseDTO

class TaskUseCases:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def create_task(self, task_dto: CreateTaskDTO) -> TaskResponseDTO:
        task = Task(
            title=task_dto.title,
            description=task_dto.description,
            due_date=task_dto.due_date,
            status="pending"
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
            due_date=task_dto.due_date
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

# app/presentation/controllers/task_controller.py
from fastapi import APIRouter, HTTPException
from typing import List
from uuid import UUID
from ...application.use_cases.task_use_cases import TaskUseCases
from ...application.dtos.task_dto import CreateTaskDTO, UpdateTaskDTO, TaskResponseDTO
from ...infrastructure.repositories.task_repository_impl import TaskRepositoryImpl

router = APIRouter()
task_repository = TaskRepositoryImpl()
task_use_cases = TaskUseCases(task_repository)

@router.post("/tasks", response_model=TaskResponseDTO)
async def create_task(task_dto: CreateTaskDTO):
    try:
        return task_use_cases.create_task(task_dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tasks/{task_id}", response_model=TaskResponseDTO)
async def get_task(task_id: UUID):
    try:
        return task_use_cases.get_task(task_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tasks", response_model=List[TaskResponseDTO])
async def get_all_tasks():
    try:
        return task_use_cases.get_all_tasks()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/tasks/{task_id}", response_model=TaskResponseDTO)
async def update_task(task_id: UUID, task_dto: UpdateTaskDTO):
    try:
        return task_use_cases.update_task(task_id, task_dto)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tasks/{task_id}/complete", response_model=TaskResponseDTO)
async def complete_task(task_id: UUID):
    try:
        return task_use_cases.complete_task(task_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: UUID):
    try:
        if task_use_cases.delete_task(task_id):
            return {"message": "Task deleted successfully"}
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# app/main.py
from fastapi import FastAPI
from .presentation.controllers.task_controller import router as task_router

app = FastAPI(title="Task Management API")

app.include_router(task_router, tags=["tasks"])

# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./tasks.db"
    api_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()

# requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.2
pydantic-settings==2.1.0
python-dotenv==1.0.0