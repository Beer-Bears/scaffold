from src.database.connection import get_pg_session
from sqlalchemy import text

async def check_pg():
    async with get_pg_session() as session:
        result = await session.execute(text("SELECT 1"))
        print(f"Postgres: {result.scalar()}")

from src.database.connection import get_neo4j_session

async def check_neo4j():
    async with get_neo4j_session() as session:
        result = await session.run("RETURN 'Neo4j connected' AS msg")
        record = await result.single()
        print(record["msg"])

async def check():
    await check_neo4j()
    await check_pg()