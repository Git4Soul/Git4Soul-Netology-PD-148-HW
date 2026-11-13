import asyncio
from itertools import batched

from aiohttp import ClientSession

from db import DbSession, Person, create_orm, close_orm

MAX_CONCURRENCY = 10
BASE_URL = "https://www.swapi.tech/api"


async def get_people_count(session: ClientSession) -> int:
    """Получаем общее количество персонажей из API."""
    async with session.get(f"{BASE_URL}/people") as response:
        data = await response.json()
        return data["total_records"]


async def get_person(session: ClientSession, person_id: int) -> dict | None:
    """Запрашиваем данные одного персонажа и извлекаем нужные поля."""
    async with session.get(f"{BASE_URL}/people/{person_id}") as response:
        if response.status != 200:
            return None
        data = await response.json()
        props = data["result"]["properties"]
        return {
            "id": person_id,
            "birth_year": props.get("birth_year"),
            "eye_color": props.get("eye_color"),
            "gender": props.get("gender"),
            "hair_color": props.get("hair_color"),
            "homeworld": props.get("homeworld"),
            "mass": props.get("mass"),
            "name": props.get("name"),
            "skin_color": props.get("skin_color"),
        }


async def save_people(people_data: list[dict]):
    """Сохраняем пачку персонажей в БД."""
    if not people_data:
        return
    async with DbSession() as db_session:
        people_orm = [Person(**person) for person in people_data]
        db_session.add_all(people_orm)
        await db_session.commit()


async def main():
    await create_orm()

    async with ClientSession() as http_session:
        total_count = await get_people_count(http_session)
        print(f"Всего персонажей для загрузки: {total_count}")

        all_ids = range(1, total_count + 1)

        for batch_ids in batched(all_ids, MAX_CONCURRENCY):
            tasks = [get_person(http_session, pid) for pid in batch_ids]
            results = await asyncio.gather(*tasks)

            valid_people = [p for p in results if p is not None]

            if valid_people:
                await save_people(valid_people)
                print(f"Сохранено {len(valid_people)} персонажей (ID {batch_ids[0]}–{batch_ids[-1]})")

    await close_orm()
    print("Загрузка завершена.")


if __name__ == "__main__":
    asyncio.run(main())