from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.washes.locations import schemas
from car_wash.washes.locations.service import CarWashLocationService

router = APIRouter(prefix='/locations', tags=['Locations'])


@router.post('', response_model=schemas.CreateResponse)
async def create_location(new_location: schemas.CarWashLocationCreate):
    location_id = await CarWashLocationService().create_entity(new_location)
    return {'location_id': location_id}


@router.get('/{id}', response_model=schemas.ReadResponse)
async def read_location(id: int):
    location = await CarWashLocationService().read_entity(id)
    return location


@router.get('', response_model=list[schemas.ReadResponse])
async def list_locations(
    query: Annotated[schemas.CarWashLocationList, Depends()],
):
    locations = await CarWashLocationService().list_entities(query)
    return locations


@router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    description='Update certain fields of existing location',
)
async def update_location(id: int, new_values: schemas.CarWashLocationUpdate):
    updated_location = await CarWashLocationService().update_entity(
        id, new_values
    )
    return updated_location


@router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_location(id: int):
    id_ = await CarWashLocationService().delete_entity(id)
    return {'detail': f'Location successfully deleted with id: {id_}'}
