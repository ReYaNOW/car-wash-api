import functools
from abc import ABC, abstractmethod

from fastapi import HTTPException
from sqlalchemy import delete, insert, select, update

from car_wash.database import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict) -> int:
        raise NotImplementedError

    async def find_one(self, id: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def find_many(self, page: int, limit: int) -> list:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> None:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    @staticmethod
    def error_handler(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            result = await func(self, *args, **kwargs)
            if result is None:
                raise HTTPException(status_code=404)
            return result

        return wrapper

    @error_handler
    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    @error_handler
    async def find_one(self, id: int) -> dict:
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id == id)
            res = await session.execute(query)
            return res.scalar()

    @error_handler
    async def find_many(self, page: int, limit: int) -> list:
        offset_value = page * limit - limit
        async with async_session_maker() as session:
            query = select(self.model).offset(offset_value).limit(limit)
            res = await session.execute(query)
            return res.scalars().all()

    @error_handler
    async def change_one(self, id: int, data: dict) -> dict:
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .values(**data)
                .where(self.model.id == id)
                .returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar()

    @error_handler
    async def delete_one(self, id: int) -> None:
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.id == id)
            await session.execute(stmt)
            await session.commit()
