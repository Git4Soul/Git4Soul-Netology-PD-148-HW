import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:

        response = await session.post(
            "http://127.0.0.1:8080/advertisements",
            json={"title": "Продам ковер", "description": "персидский", "owner": "Андрей"},
        )
        print("POST:", response.status, await response.json())

        response = await session.get("http://127.0.0.1:8080/advertisements")
        print("GET ALL:", response.status, await response.json())

        response = await session.patch(
            "http://127.0.0.1:8080/advertisements/1",
            json={"title": "Продам ковер недорого"},
        )
        print("PATCH:", response.status, await response.json())

        response = await session.delete("http://127.0.0.1:8080/advertisements/1")
        print("DELETE:", response.status, await response.json())

        response = await session.get("http://127.0.0.1:8080/advertisements/1")
        print("GET AFTER DELETE:", response.status, await response.json())


asyncio.run(main())