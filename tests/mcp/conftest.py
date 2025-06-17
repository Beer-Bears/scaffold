import pytest
from httpx import AsyncClient
from src.mcp.server import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client