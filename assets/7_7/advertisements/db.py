import atexit
import datetime
import os

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedColumn,
    mapped_column,
    sessionmaker,
)

POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ads")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

POSTGRES_DSN = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(POSTGRES_DSN)
atexit.register(engine.dispose)

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Advertisement(Base):
    __tablename__ = "advertisements"

    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    title: MappedColumn[str] = mapped_column(String(200), nullable=False)
    description: MappedColumn[str] = mapped_column(String(1000), nullable=True)
    created_at: MappedColumn[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    owner: MappedColumn[str] = mapped_column(String(100), nullable=False)

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": int(self.created_at.timestamp()) if self.created_at else None,
            "owner": self.owner,
        }

    @property
    def id_dict(self):
        return {"id": self.id}


Base.metadata.create_all(bind=engine)