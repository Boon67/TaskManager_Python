# app/main.py
from fastapi import FastAPI
from .presentation.controllers.task_controller import router as task_router

app = FastAPI(title="Task Management API")

app.include_router(task_router, tags=["tasks"])
