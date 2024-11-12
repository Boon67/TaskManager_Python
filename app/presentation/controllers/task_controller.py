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
