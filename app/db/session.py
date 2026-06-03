# Following article explains about setting
# Session for database https://fastapi.tiangolo.com/tutorial/sql-databases/

from typing import Generator
from contextvars import ContextVar

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.db.config import db_config

engine = create_engine(db_config.database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as db:
        yield db


db_session: ContextVar[Session] = ContextVar('db_session', default=next(get_db()))
