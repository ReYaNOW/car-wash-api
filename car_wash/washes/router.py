from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.washes import schemas
from car_wash.washes.locations.router import router as locations_router
from car_wash.washes.service import CarWashService

router = APIRouter(prefix='/car_washes', tags=['CarWashes'])

sub_router = APIRouter(prefix='/car_washes', tags=['CarWashLocations'])

sub_router.include_router(locations_router)


@router.post('', response_model=schemas.CreateResponse)
async def create_car_wash(new_car_wash: schemas.CarWashCreate):
    car_wash_id = await CarWashService().create_entity(new_car_wash)
    return {'car_wash_id': car_wash_id}


@router.get('/{id}', response_model=schemas.ReadResponse)
async def read_car_wash(id: int):
    car_wash = await CarWashService().read_entity(id)
    return car_wash


@router.get('', response_model=list[schemas.ReadResponse])
async def list_car_washes(query: Annotated[schemas.CarWashList, Depends()]):
    car_washes = await CarWashService().paginate_entities(query)
    return car_washes


@router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    description='Update certain fields of existing car wash',
)
async def update_car_wash(id: int, new_values: schemas.CarWashUpdate):
    updated_car_wash = await CarWashService().update_entity(id, new_values)
    return updated_car_wash


@router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_car_wash(id: int):
    id_ = await CarWashService().delete_entity(id)
    return {'detail': f'Car wash successfully deleted with id: {id_}'}
