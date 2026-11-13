import os
from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_USER = os.getenv("POSTGRES_USER", "swapi")
POSTGRES_DB = os.getenv("POSTGRES_DB", "swapi")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DB_DSN = (
    f"postgresql+asyncpg://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)
engine = create_async_engine(DB_DSN)
DbSession = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class Person(Base):
    __tablename__ = "people"

    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    birth_year: MappedColumn[str] = mapped_column(String(50), nullable=True)
    eye_color: MappedColumn[str] = mapped_column(String(50), nullable=True)
    gender: MappedColumn[str] = mapped_column(String(50), nullable=True)
    hair_color: MappedColumn[str] = mapped_column(String(50), nullable=True)
    homeworld: MappedColumn[str] = mapped_column(String(255), nullable=True)
    mass: MappedColumn[str] = mapped_column(String(50), nullable=True)
    name: MappedColumn[str] = mapped_column(String(100), nullable=False)
    skin_color: MappedColumn[str] = mapped_column(String(50), nullable=True)

async def create_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()
