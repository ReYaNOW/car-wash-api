import pydantic

from car_wash.utils.repository import AbstractRepository
from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class GenericCRUDService:
    repository: type(AbstractRepository) = None

    def __init__(self):
        self.crud_repo: AbstractRepository = self.repository()

    async def create_entity(self, new_entity: pydantic.BaseModel):
        entity_dict = new_entity.model_dump()
        entity_id = await self.crud_repo.add_one(entity_dict)
        return entity_id

    async def read_entity(self, id: int):
        entity = await self.crud_repo.find_one(id, load_children=True)
        return entity

    async def paginate_entities(self, query: GenericListRequest):
        query = query.model_dump()
        page, limit, order_by = (
            query.pop('page'),
            query.pop('limit'),
            query.pop('order_by'),
        )
        filters = {k: v for k, v in query.items() if v is not None}

        entities = await self.crud_repo.find_many(
            page, limit, order_by, filters, load_children=True
        )
        total_records = await self.crud_repo.count_records(filters)
        pages = (total_records + limit - 1) // limit
        return GenericListResponse(data=entities, total=pages, current=page)

    async def update_entity(self, id: int, new_values: pydantic.BaseModel):
        new_values_dict = new_values.model_dump(exclude_none=True)
        updated_entity = await self.crud_repo.change_one(id, new_values_dict)
        return updated_entity

    async def delete_entity(self, id: int) -> int:
        id_ = await self.crud_repo.delete_one(id)
        return id_
