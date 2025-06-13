from contextlib import asynccontextmanager
from typing import AsyncGenerator

from neo4j import AsyncGraphDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.database.config import settings

# --- PostgreSQL ---
engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@asynccontextmanager
async def get_pg_session():
    """
    How use:
    .. code-block:: python

        async with get_pg_session() as session:
            result = await session...
    """
    async with AsyncSessionLocal() as session:
        yield session


# --- Neo4j ---
neo4j_driver = AsyncGraphDatabase.driver(
    settings.neo4j_uri,
    auth=(settings.neo4j_user, settings.neo4j_password)
)

@asynccontextmanager
async def get_neo4j_session():
    """
    How use:
    .. code-block:: python

        async with get_neo4j_session() as session:
            result = await session...
    """
    async with neo4j_driver.session() as session:
        yield session
