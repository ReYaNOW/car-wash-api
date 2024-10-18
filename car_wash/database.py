from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from car_wash.config import config

db_url = config.database_url.unicode_string()


async_url = db_url.replace('postgresql', 'postgresql+asyncpg')
async_engine = create_async_engine(
    async_url, pool_recycle=1800, pool_pre_ping=True
)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
