from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine,SQLModel,Session
from sqlalchemy import text
from .config import settings


postgres_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(postgres_url)


def create_database():
    SQLModel.metadata.create_all(engine)
    with engine.connect() as conn:
        conn.execute(
            text("""
                SELECT setval(
                    pg_get_serial_sequence('"posts"', 'id'),
                    COALESCE(MAX(id), 1)
                ) FROM "posts";
            """)
        )
        conn.commit()


def create_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session,Depends(create_session)]
