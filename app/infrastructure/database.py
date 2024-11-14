# /app/infrastructure/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

load_dotenv()


# Configuration options
DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # Default to SQLite if not set
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", None)
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_USER = os.getenv("DB_USER", "myuser")
DB_PASS = os.getenv("DB_PASS", "mypassword")


def get_db_engine():
    if DB_TYPE == "sqlite":
        return create_engine(f"sqlite:///{DB_NAME}.db")
    elif DB_TYPE == "cockroachdb":
        return create_engine(
            f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=verify-full"
        )
    elif DB_TYPE == "postgresql":
        return create_engine(
            f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        raise ValueError(f"Invalid DB_TYPE: {DB_TYPE}")


def get_db_session():
    """
    Create a SQLAlchemy session based on the database engine.
    """
    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()


engine = get_db_engine()
SessionLocal = get_db_session
Base = declarative_base()
