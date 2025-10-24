
from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings
from contextlib import contextmanager

engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # echo=True is great for debugging, it logs all SQL queries
)

def create_db_and_tables():
    """
    Creates all database tables defined by SQLModel.
    This is called once on application startup.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Dependency function to get a database session per request.
    """
    with Session(engine) as session:
        yield session

@contextmanager
def get_task_session():
    """
    Provides a database session for use inside Celery tasks.
    Ensures the session is always closed.
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()