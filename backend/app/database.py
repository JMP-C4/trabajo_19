"""Database configuration and session management."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/tasks",
)

# `future=True` for 2.x style behavior, `echo` toggled via env for debugging.
engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=os.getenv("SQL_DEBUG", "0") == "1",
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


def get_db():
    """FastAPI dependency to provide a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
