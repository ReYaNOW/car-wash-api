from typing import Generic

from fastapi import HTTPException
from pydantic import BaseModel

from car_wash.utils.repository import SQLAlchemyRepository, T
from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class GenericCRUDService(Generic[T]):
    repository: type[SQLAlchemyRepository]

    def __init__(self):
        self.crud_repo: SQLAlchemyRepository = self.repository()

    async def create_entities(
        self, new_entity: BaseModel | list[BaseModel]
    ) -> int | list[int]:
        if isinstance(new_entity, list):
            entities_dict = [entity.model_dump() for entity in new_entity]
            entity_ids = await self.crud_repo.add_many(entities_dict)
            return entity_ids
        entities_dict = new_entity.model_dump()
        entity_id = await self.crud_repo.add_one(entities_dict)
        return entity_id

    async def read_entity(self, id: int) -> T:
        entity: T = await self.crud_repo.find_one(id)
        if entity is None:
            raise HTTPException(status_code=404)
        return entity

    async def paginate_entities(
        self, query: GenericListRequest
    ) -> GenericListResponse:
        query = query.model_dump()
        page, limit, order_by = (
            query.pop('page'),
            query.pop('limit'),
            query.pop('order_by'),
        )
        filters = {k: v for k, v in query.items() if v is not None}

        entities = await self.crud_repo.find_many(
            page, limit, order_by, filters
        )
        total_records = await self.crud_repo.count_records(filters)
        pages = (total_records + limit - 1) // limit
        return GenericListResponse(data=entities, total=pages, current=page)

    async def update_entity(self, id: int, new_values: BaseModel) -> T:
        new_values_dict = new_values.model_dump(exclude_none=True)
        updated_entity = await self.crud_repo.change_one(id, new_values_dict)
        if updated_entity is None:
            raise HTTPException(status_code=404)
        return updated_entity

    async def delete_entity(self, id: int) -> int:
        id_ = await self.crud_repo.delete_one(id)
        if id_ is None:
            raise HTTPException(status_code=404)
        return id_
