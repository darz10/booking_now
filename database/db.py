from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import settings

SQLALCHEMY_DATABASE_URL = settings.DB_CONNECT

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def create_db() -> None:
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
