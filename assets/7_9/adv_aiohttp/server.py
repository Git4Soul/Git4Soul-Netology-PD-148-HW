import json

from aiohttp import web
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db import Session, Advertisement, init_db, close_db
from errors import HttpError
from schema import CreateAdvertisement, UpdateAdvertisement, validate


def get_error(error_cls: type, message: dict | str | list):
    message = {"error": message}
    message_str = json.dumps(message)
    raise error_cls(
        text=message_str,
        content_type="application/json",
    )


async def orm_context(app: web.Application):
    print("START DB")
    await init_db()
    yield
    await close_db()
    print("END DB")


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


@web.middleware
async def error_middleware(request: web.Request, handler):
    try:
        return await handler(request)
    except HttpError as err:
        return web.json_response(
            {"error": err.message},
            status=err.status_code,
        )
    except web.HTTPException as err:
        return web.json_response(
            {"error": err.reason},
            status=err.status_code,
        )


class AdvertisementView(web.View):

    @property
    def session(self) -> AsyncSession:
        return self.request.session

    @property
    def advertisement_id(self) -> int | None:
        adv_id = self.request.match_info.get("advertisement_id")
        return int(adv_id) if adv_id else None

    async def get_advertisement(self) -> Advertisement:
        advertisement = await self.session.get(Advertisement, self.advertisement_id)
        if advertisement is None:
            raise HttpError("advertisement not found", 404)
        return advertisement

    async def add_advertisement(self, advertisement: Advertisement):
        self.session.add(advertisement)
        try:
            await self.session.commit()
        except IntegrityError:
            raise HttpError("advertisement already exists", 400)


    async def get(self):
        if self.advertisement_id is None:
            result = await self.session.execute(select(Advertisement))
            advertisements = result.scalars().all()
            return web.json_response([ad.json for ad in advertisements])

        advertisement = await self.get_advertisement()
        return web.json_response(advertisement.json)

    async def post(self):
        json_data = await self.request.json()
        validated = validate(json_data, CreateAdvertisement)
        advertisement = Advertisement(
            title=validated["title"],
            description=validated.get("description"),
            owner=validated["owner"],
        )
        await self.add_advertisement(advertisement)
        return web.json_response(advertisement.id_json, status=201)

    async def patch(self):
        json_data = await self.request.json()
        validated = validate(json_data, UpdateAdvertisement)
        advertisement = await self.get_advertisement()

        if "title" in validated:
            advertisement.title = validated["title"]
        if "description" in validated:
            advertisement.description = validated["description"]
        if "owner" in validated:
            advertisement.owner = validated["owner"]

        await self.add_advertisement(advertisement)
        return web.json_response(advertisement.json)

    async def delete(self):
        advertisement = await self.get_advertisement()
        await self.session.delete(advertisement)
        await self.session.commit()
        return web.json_response({"message": "deleted"})


app = web.Application()

app.cleanup_ctx.append(orm_context)
app.middlewares.append(error_middleware)
app.middlewares.append(session_middleware)

app.add_routes([
    web.get(r"/advertisements", AdvertisementView),
    web.post(r"/advertisements", AdvertisementView),
    web.get(r"/advertisements/{advertisement_id:\d+}", AdvertisementView),
    web.patch(r"/advertisements/{advertisement_id:\d+}", AdvertisementView),
    web.delete(r"/advertisements/{advertisement_id:\d+}", AdvertisementView),
])

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)