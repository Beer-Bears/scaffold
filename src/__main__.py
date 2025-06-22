import asyncio
from src.database.check import check as test_db
from src.mcp.server import mcp

if __name__ == '__main__':
    print("Hello, Scaffold!")
    asyncio.run(test_db())
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)