from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import (
    BinaryExpression,
    and_,
    delete,
    func,
    insert,
    orm,
    select,
    update,
)
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.expression import Select

from car_wash.database import async_session_maker
from car_wash.utils.exception_handling import orm_errors_handler


class AnyModel(orm.MappedClassProtocol[Any]):
    __tablename__ = 'any_model'

    id: orm.Mapped[int]


class AbstractRepository(ABC):
    model: type[AnyModel]

    @abstractmethod
    async def add_one(self, data: dict) -> int:
        raise NotImplementedError

    async def find_one(
        self, id: int, load_children: list | None = None
    ) -> AnyModel:
        raise NotImplementedError

    async def find_one_by_custom_field(
        self,
        custom_field: str,
        custom_value: str | int,
        relationships: list | None = None,
    ) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def find_many(
        self,
        page: int,
        limit: int,
        order_by: str,
        filter_by: dict,
        relationships: list | None = None,
    ) -> list[AnyModel]:
        raise NotImplementedError

    @abstractmethod
    async def change_one(self, id: int, data: dict) -> AnyModel:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    async def count_records(self, filters: dict) -> int:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    @orm_errors_handler
    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    @orm_errors_handler
    async def find_one(
        self, id: int, relationships: list | None = None
    ) -> AnyModel:
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id == id)
            query = self.add_joined_loads(query, relationships)

            res = await session.execute(query)
            return res.scalar()

    @orm_errors_handler
    async def find_one_by_custom_field(
        self,
        custom_field: str,
        custom_value: str | int,
        relationships: list | None = None,
    ) -> AnyModel:
        column: orm.MappedColumn = getattr(self.model, custom_field)
        async with async_session_maker() as session:
            query = select(self.model).where(column == custom_value)
            query = self.add_joined_loads(query, relationships)

            res = await session.execute(query)
            return res.scalar()

    @orm_errors_handler
    async def find_many(
        self,
        page: int,
        limit: int,
        order_by: str,
        filters: dict,
        relationships: list | None = None,
    ) -> list[AnyModel]:
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

            query = self.add_joined_loads(query, relationships)

            res = await session.execute(query)
            return res.unique().scalars().all()

    @orm_errors_handler
    async def count_records(self, filters: dict) -> int:
        async with async_session_maker() as session:
            query = select(func.count()).select_from(self.model)

            if filters:
                expressions = self.get_expressions(filters)
                query = query.where(and_(*expressions))

            res = await session.execute(query)
            return res.scalar_one()

    @orm_errors_handler
    async def change_one(self, id: int, data: dict) -> AnyModel:
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

    @orm_errors_handler
    async def change_one_by_custom_field(
        self, custom_field: str, custom_value: str | int, data: dict
    ) -> AnyModel:
        column: orm.MappedColumn = getattr(self.model, custom_field)
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

    @orm_errors_handler
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

    def add_joined_loads(
        self, query: Select, relationships: list[InstrumentedAttribute]
    ) -> Select:
        if not relationships:
            return query
        joined_loads = [
            orm.joinedload(relationship) for relationship in relationships
        ]
        return query.options(*joined_loads)

    def get_expressions(
        self, filters: dict[str, str | int]
    ) -> list[BinaryExpression]:
        expressions = []
        for k, v in filters.items():
            if k.endswith('_like'):
                column: orm.MappedColumn = getattr(
                    self.model, k.split('_like')[0]
                )
                expressions.append(column.ilike(f'%{v}%'))
            else:
                column: orm.MappedColumn = getattr(self.model, k)
                expressions.append(column == v)
        return expressions
