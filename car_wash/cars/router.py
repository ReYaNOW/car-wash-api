from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends

from car_wash.cars import schemas
from car_wash.cars.body_types.router import router as body_types_router
from car_wash.cars.brands.router import router as brands_router
from car_wash.cars.car_models.router import router as car_models_router
from car_wash.cars.configurations.router import router as configurations_router
from car_wash.cars.generations.router import router as generations_router
from car_wash.cars.service import UserCarService
from car_wash.config import config

router = APIRouter(prefix='/cars', tags=['Cars'])

# Creating separate router to separate those routes from Cars tag
# in swagger doc

sub_router = APIRouter(
    prefix='/cars',
    tags=[
        'CarBrands, CarModels, CarGenerations, CarBodyTypes, CarConfiguration'
    ],
)

sub_router.include_router(brands_router)
sub_router.include_router(car_models_router)
sub_router.include_router(generations_router)
sub_router.include_router(body_types_router)
sub_router.include_router(configurations_router)


@router.post('', response_model=schemas.CreateResponse)
async def create_user_car(new_car: schemas.UserCarCreate):
    user_car_id = await UserCarService().create_entity(new_car)
    return {'user_car_id': user_car_id}


@router.get('/{id}', response_model=schemas.ReadResponse)
async def read_user_car(id: int):
    user_car = await UserCarService().read_entity(id)
    return user_car


@router.get('', response_model=list[schemas.ReadResponse])
async def list_user_cars(query: Annotated[schemas.UserCarList, Depends()]):
    user_cars = await UserCarService().list_entities(query)
    return user_cars


@router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    description='Update certain fields of existing user car',
)
async def update_car(id: int, new_values: schemas.UserCarUpdate):
    updated_user_car = await UserCarService().update_entity(id, new_values)
    return updated_user_car


@router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_car(id: int):
    id_ = await UserCarService().delete_entity(id)
    return {'detail': f'User car successfully deleted with id: {id_}'}


if config.debug:
    from car_wash.utils.fill_db_with_cars import fill_db

    @router.post('/fill_db_with_cars')
    async def fill_db_with_cars(background_tasks: BackgroundTasks):
        if config.filling_db:
            return 'Database is already filling up'
        background_tasks.add_task(fill_db)
        config.filling_db = True
        return 'Started filling database with cars data'
