from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.utils.routers import get_admin_router, get_client_router
from car_wash.washes.additions import schemas
from car_wash.washes.additions.service import CarWashAdditionService

router = APIRouter()

client_router = get_client_router('/additions', tags=['CarWashes|Additions'])
admin_router = get_admin_router('/additions', tags=['CarWashes|Additions'])


@admin_router.post('', response_model=schemas.CreateResponse)
async def create_addition(new_prices: schemas.CarWashAdditionCreate):
    addition_id = await CarWashAdditionService().create_entities(new_prices)
    return {'car_wash_addition_id': addition_id}


@admin_router.post('/bulk', response_model=schemas.CreateBulkResponse)
async def create_additions(new_prices: list[schemas.CarWashAdditionCreate]):
    addition_ids = await CarWashAdditionService().create_entities(new_prices)
    return {'car_wash_addition_ids': addition_ids}


@client_router.get('/{id}', response_model=schemas.ReadResponse)
async def read_addition(id: int):
    addition = await CarWashAdditionService().read_entity(id)
    return addition


@client_router.get('', response_model=schemas.ListResponse)
async def list_additions(
    query: Annotated[schemas.CarWashAdditionList, Depends()],
):
    prices = await CarWashAdditionService().paginate_entities(query)
    return prices


@admin_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    summary='Update certain fields of existing addition',
)
async def update_addition(id: int, new_values: schemas.CarWashAdditionUpdate):
    updated_addition = await CarWashAdditionService().update_entity(
        id, new_values
    )
    return updated_addition


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_price(id: int):
    id_ = await CarWashAdditionService().delete_entity(id)
    return {'detail': f'Addition successfully deleted with id: {id_}'}


router.include_router(admin_router)
router.include_router(client_router)
