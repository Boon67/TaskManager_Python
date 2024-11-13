# app/main.py
from fastapi import FastAPI
from .presentation.controllers.task_controller import router as task_router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Task Management API")

app.include_router(task_router, tags=["tasks"])

# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = os.getenv("DB_URL")
    api_prefix: str = "/api/v1"


#    class Config:
#        env_file = ".env"


settings = Settings()
