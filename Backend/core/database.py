# Backend/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from Backend.core.settings import Settings

db_url = Settings().DATABASE_URL

if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif "+psycopg2" in db_url:
    db_url = db_url.replace("+psycopg2", "+asyncpg")

engine = create_async_engine(db_url, echo=False)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    async with async_session() as session:
        yield session

@asynccontextmanager
async def get_session_context():
    """Context manager para uso standalone (sem FastAPI Depends)"""
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session