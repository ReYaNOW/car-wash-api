from car_wash.cars.body_types.repository import CarBodyTypeRepository
from car_wash.cars.models import CarBodyType
from car_wash.utils.schemas import GenericListRequest, GenericListResponse
from car_wash.utils.service import GenericCRUDService


class CarBodyTypeService(GenericCRUDService[CarBodyType]):
    repository = CarBodyTypeRepository

    async def paginate_necessary_bts(
        self, query: GenericListRequest
    ) -> GenericListResponse:
        query = query.model_dump()
        page, limit, order_by = (
            query.pop('page'),
            query.pop('limit'),
            query.pop('order_by'),
        )
        filters = {k: v for k, v in query.items() if v is not None}
        filters['parent_id'] = None

        entities = await self.crud_repo.find_many(
            page, limit, order_by, filters
        )
        total_records = await self.crud_repo.count_records(filters)
        pages = (total_records + limit - 1) // limit
        return GenericListResponse(data=entities, total=pages, current=page)
