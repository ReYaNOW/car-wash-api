from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.utils.routers import get_admin_router, get_client_router
from car_wash.washes.prices import schemas
from car_wash.washes.prices.service import CarWashPriceService

router = APIRouter()

client_router = get_client_router('/prices', tags=['CarWashes|Prices'])
admin_router = get_admin_router('/prices', tags=['CarWashes|Prices'])


@admin_router.post('', response_model=schemas.CreateResponse)
async def create_price(new_prices: schemas.CarWashPriceCreate):
    price_id = await CarWashPriceService().create_entities(new_prices)
    return {'car_wash_price_id': price_id}


@admin_router.post('/bulk', response_model=schemas.CreateBulkResponse)
async def create_prices(new_prices: list[schemas.CarWashPriceCreate]):
    price_ids = await CarWashPriceService().create_entities(new_prices)
    return {'car_wash_price_ids': price_ids}


@client_router.get('/{id}', response_model=schemas.ReadResponse)
async def read_price(id: int):
    price = await CarWashPriceService().read_entity(id)
    return price


@client_router.get('', response_model=schemas.ListResponse)
async def list_prices(
    query: Annotated[schemas.CarWashPriceList, Depends()],
):
    prices = await CarWashPriceService().paginate_entities(query)
    return prices


@admin_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    summary='Update certain fields of existing price',
)
async def update_price(id: int, new_values: schemas.CarWashPriceUpdate):
    updated_price = await CarWashPriceService().update_entity(id, new_values)
    return updated_price


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_price(id: int):
    id_ = await CarWashPriceService().delete_entity(id)
    return {'detail': f'Price successfully deleted with id: {id_}'}


router.include_router(admin_router)
router.include_router(client_router)
