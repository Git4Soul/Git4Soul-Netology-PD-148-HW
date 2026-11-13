import asyncio
from db import create_orm, close_orm

async def main():
    await create_orm()
    print("Таблицы созданы.")
    await close_orm()

if __name__ == "__main__":
    asyncio.run(main())