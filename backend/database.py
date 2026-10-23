from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# the server is ran from backend/ so we reference ./
DATABASE_URL = "sqlite+aiosqlite:///./app.db"

# set same thread to false for compatibility with SQLite on FastAPI
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

# Async database session
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# create session with db
# SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

# Create and set up async db session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        """