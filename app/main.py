# app/main.py
from fastapi import FastAPI
import uvicorn
from .presentation.controllers.task_controller import router as task_router

app = FastAPI(title="Task Management API")


app.include_router(task_router, tags=["tasks"])
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
