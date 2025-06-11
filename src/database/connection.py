from contextlib import asynccontextmanager

from neomodel import config
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
def init_neo4j():
    """
    call in main
    """
    config.DATABASE_URL = settings.neo4j_uri
