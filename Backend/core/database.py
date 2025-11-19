# Backend/core/database.py
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from Backend.core.settings import Settings

database_url = Settings().DATABASE_URL

# Converter qualquer formato PostgreSQL para asyncpg
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif database_url.startswith("postgres://"):  # Fly.io usa esse formato
    database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif "psycopg2" in database_url:
    database_url = database_url.replace("psycopg2", "asyncpg")

# Criar engine async
engine = create_async_engine(
    database_url,
    echo=False,
    pool_pre_ping=True,
)

# Sessão async
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