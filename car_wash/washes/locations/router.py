from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.utils.router import get_admin_router, get_client_router
from car_wash.washes.locations import schemas
from car_wash.washes.locations.service import CarWashLocationService

router = APIRouter(tags=['Locations'])

client_router = get_client_router('/locations')
admin_router = get_admin_router('/locations')


@admin_router.post('', response_model=schemas.CreateResponse)
async def create_location(new_location: schemas.CarWashLocationCreate):
    location_id = await CarWashLocationService().create_entity(new_location)
    return {'location_id': location_id}


@client_router.get('/{id}', response_model=schemas.ReadResponse)
async def read_location(id: int):
    location = await CarWashLocationService().read_entity(id)
    return location


@client_router.get('', response_model=schemas.ListResponse)
async def list_locations(
    query: Annotated[schemas.CarWashLocationList, Depends()],
):
    locations = await CarWashLocationService().paginate_entities(query)
    return locations


@admin_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    summary='Update certain fields of existing location',
)
async def update_location(id: int, new_values: schemas.CarWashLocationUpdate):
    updated_location = await CarWashLocationService().update_entity(
        id, new_values
    )
    return updated_location


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_location(id: int):
    id_ = await CarWashLocationService().delete_entity(id)
    return {'detail': f'Location successfully deleted with id: {id_}'}


router.include_router(client_router)
router.include_router(admin_router)
