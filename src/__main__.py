import asyncio
from src.database.check import check as test_db

if __name__ == '__main__':
    print("Hello, Scaffold!")
    asyncio.run(test_db())