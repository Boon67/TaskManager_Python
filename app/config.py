from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./tasks.db"
    api_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()
