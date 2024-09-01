import functools
from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import and_, delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import MappedColumn, joinedload

from car_wash.database import async_session_maker
from car_wash.utils.exception_handling import handle_integrity_error
from car_wash.utils.schemas import T


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict) -> int:
        raise NotImplementedError

    async def find_one(self, id: int, load_children: list | None = None) -> T:
        raise NotImplementedError

    async def find_one_by_custom_field(
        self,
        custom_field: str,
        custom_value: Any,
        load_children: list | None = None,
    ) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def find_many(
        self,
        page: int,
        limit: int,
        order_by: str,
        filter_by: dict,
        load_children: list | None = None,
    ) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def change_one(self, id: int, data: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    async def count_records(self, filters: dict):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    @staticmethod
    def error_handler(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                result = await func(self, *args, **kwargs)
                return result
            except IntegrityError as e:
                handle_integrity_error(e, self.model.__tablename__)

        return wrapper

    @error_handler
    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    @error_handler
    async def find_one(self, id: int, load_children: list | None = None) -> T:
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id == id)

            if load_children:
                joined_loads = self.get_joined_loads(load_children)
                query = query.options(*joined_loads)

            res = await session.execute(query)
            return res.scalar()

    @error_handler
    async def find_one_by_custom_field(
        self,
        custom_field: str,
        custom_value: Any,
        load_children: list | None = None,
    ) -> T:
        column: MappedColumn = getattr(self.model, custom_field)
        async with async_session_maker() as session:
            query = select(self.model).where(column == custom_value)

            if load_children:
                joined_loads = self.get_joined_loads(load_children)
                query = query.options(*joined_loads)

            res = await session.execute(query)
            return res.scalar()

    @error_handler
    async def find_many(
        self,
        page: int,
        limit: int,
        order_by: str,
        filters: dict,
        load_children: list | None = None,
    ) -> list[T]:
        offset_value = page * limit - limit
        async with async_session_maker() as session:
            query = (
                select(self.model)
                .offset(offset_value)
                .limit(limit)
                .order_by(order_by)
            )
            if filters:
                expressions = self.get_expressions(filters)
                query = query.where(and_(*expressions))

            if load_children:
                joined_loads = self.get_joined_loads(load_children)
                query = query.options(*joined_loads)

            res = await session.execute(query)
            return res.unique().scalars().all()

    async def count_records(self, filters: dict) -> int:
        async with async_session_maker() as session:
            query = select(func.count()).select_from(self.model)

            if filters:
                expressions = self.get_expressions(filters)
                query = query.where(and_(*expressions))

            res = await session.execute(query)
            return res.scalar_one()

    @error_handler
    async def change_one(self, id: int, data: dict) -> T:
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
    async def change_one_by_custom_field(
        self, custom_field: str, custom_value: Any, data: dict
    ) -> T:
        column: MappedColumn = getattr(self.model, custom_field)
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .values(**data)
                .where(column == custom_value)
                .returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar()

    @error_handler
    async def delete_one(self, id: int) -> int:
        async with async_session_maker() as session:
            stmt = (
                delete(self.model)
                .where(self.model.id == id)
                .returning(self.model.id)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res

    def get_joined_loads(self, relationships):
        return [joinedload(relationship) for relationship in relationships]

    def get_expressions(self, filters):
        expressions = []
        for k, v in filters.items():
            k: str
            if k.endswith('_like'):
                column: MappedColumn = getattr(self.model, k.split('_like')[0])
                expressions.append(column.ilike(f'%{v}%'))
            else:
                column: MappedColumn = getattr(self.model, k)
                expressions.append(column == v)

        return expressions
