from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.cars.body_types import schemas
from car_wash.cars.body_types.service import CarBodyTypeService
from car_wash.utils.router import get_admin_router, get_client_router

router = APIRouter()

client_router = get_client_router('/body_types', tags=['Cars|BodyTypes'])
admin_router = get_admin_router('/body_types', tags=['Cars|BodyTypes'])


@admin_router.post('', response_model=schemas.CreateResponse)
async def create_body_type(new_body_type: schemas.BodyTypeCreate):
    body_type_id = await CarBodyTypeService().create_entity(new_body_type)
    return {'body_type_id': body_type_id}


@client_router.get('/{id}', response_model=schemas.ReadResponse)
async def read_body_type(id: int):
    body_type = await CarBodyTypeService().read_entity(id)
    return body_type


@client_router.get('', response_model=schemas.ListResponse)
async def list_body_types(query: Annotated[schemas.BodyTypeList, Depends()]):
    paginated_body_types = await CarBodyTypeService().paginate_entities(query)
    return paginated_body_types


@admin_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    summary='Update certain fields of existing body type',
)
async def update_body_type(id: int, new_values: schemas.BodyTypeUpdate):
    updated_body_type = await CarBodyTypeService().update_entity(
        id, new_values
    )
    return updated_body_type


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_body_type(id: int):
    id_ = await CarBodyTypeService().delete_entity(id)
    return {'detail': f'Body type successfully deleted with id: {id_}'}


router.include_router(admin_router)
router.include_router(client_router)
