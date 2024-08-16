from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.cars import schemas
from car_wash.cars.body_types.router import router as body_types_router
from car_wash.cars.brands.router import router as brands_router
from car_wash.cars.generations.router import router as generations_router
from car_wash.cars.service import CarService

router = APIRouter(prefix='/cars', tags=['Cars'])

# Creating separate router to separate those routes from Cars tag
# in swagger doc

sub_router = APIRouter(
    prefix='/cars', tags=['CarBodyTypes, CarBrands, CarGenerations']
)

sub_router.include_router(body_types_router)
sub_router.include_router(brands_router)
sub_router.include_router(generations_router)


@router.post('', response_model=schemas.CreateResponse)
async def create_car(new_car: schemas.CarCreate):
    car_id = await CarService().create_entity(new_car)
    return {'car_id': car_id}


@router.get('/{id}', response_model=schemas.ReadResponse)
async def read_car(id: int):
    car = await CarService().read_entity(id)
    return car


@router.get('', response_model=list[schemas.ReadResponse])
async def list_cars(query: Annotated[schemas.CarList, Depends()]):
    cars = await CarService().list_entities(query)
    return cars


@router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    description='Update certain fields of existing car',
)
async def update_car(id: int, new_values: schemas.CarUpdate):
    updated_car = await CarService().update_entity(id, new_values)
    return updated_car


@router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_car(id: int):
    id_ = await CarService().delete_entity(id)
    return {'detail': f'Car successfully deleted with id: {id_}'}
