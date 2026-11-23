# app/app.py

from typing import Annotated, Optional
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from dependencies import get_db_session
from lifespan import lifespan
from services import add_item, get_item, update_item, delete_item, search_items

app = FastAPI(
    title="Advertisement Service API",
    description="API для сервиса объявлений купли/продажи",
    version="0.0.1",
    lifespan=lifespan
)

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


@app.post("/advertisement", response_model=schemas.CreateAdvertisementResponse, summary="Создать новое объявление")
async def create_advertisement(
        ad_data: schemas.CreateAdvertisementRequest,
        session: SessionDep
):
    new_ad = await add_item(session, models.Advertisement, ad_data)
    return schemas.CreateAdvertisementResponse(id=new_ad.id)


@app.get("/advertisement/{advertisement_id}", response_model=schemas.GetAdvertisementResponse, summary="Получить объявление по ID")
async def get_advertisement(
        advertisement_id: int,
        session: SessionDep
):
    ad = await get_item(session, models.Advertisement, advertisement_id)
    return schemas.GetAdvertisementResponse(**ad.to_dict())


@app.patch("/advertisement/{advertisement_id}", response_model=schemas.UpdateAdvertisementResponse, summary="Обновить объявление")
async def update_advertisement(
        advertisement_id: int,
        update_data: schemas.UpdateAdvertisementRequest,
        session: SessionDep
):
    updated_ad = await update_item(session, models.Advertisement, advertisement_id, update_data)
    return schemas.UpdateAdvertisementResponse(**updated_ad.to_dict())


@app.delete("/advertisement/{advertisement_id}", response_model=schemas.OKResponse, summary="Удалить объявление")
async def delete_advertisement(
        advertisement_id: int,
        session: SessionDep
):
    await delete_item(session, models.Advertisement, advertisement_id)
    return schemas.OKResponse()


@app.get("/advertisement", response_model=list[schemas.GetAdvertisementResponse], summary="Поиск объявлений по полям")
async def search_advertisements(
        session: SessionDep,
        title: Optional[str] = None,
        author: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
):
    ads = await search_items(
        session, models.Advertisement,
        title=title, author=author, price_min=price_min, price_max=price_max
    )
    return [schemas.GetAdvertisementResponse(**ad.to_dict()) for ad in ads]