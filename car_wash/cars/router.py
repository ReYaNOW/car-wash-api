from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends

from car_wash.auth.dependencies import (
    get_user_client,
    get_validate_access_to_entity,
    get_validate_query_user_id,
)
from car_wash.cars import schemas
from car_wash.cars.models import UserCar
from car_wash.cars.service import UserCarService
from car_wash.config import config
from car_wash.users.models import User
from car_wash.utils.router import OWNER, get_client_router, get_owner_router

router = APIRouter(tags=['Cars'])

client_router = get_client_router('/cars')
client_owner_router = get_owner_router('/cars', UserCarService)


@client_router.post('', response_model=schemas.CreateResponse)
async def create_user_car(
    user: Annotated[User, Depends(get_user_client)],
    new_car: schemas.UserCarCreate,
):
    user_car_id = await UserCarService().create_user_car(user, new_car)
    return {'user_car_id': user_car_id}


@client_owner_router.get('/{id}', response_model=schemas.ReadResponse)
async def read_user_car(
    user_car: Annotated[
        UserCar, Depends(get_validate_access_to_entity(UserCarService))
    ],
):
    return user_car


@client_router.get('', response_model=schemas.ListResponse, description=OWNER)
async def list_user_cars(
    query: Annotated[
        schemas.UserCarList,
        Depends(get_validate_query_user_id(schemas.UserCarList)),
    ],
):
    paginated_cars = await UserCarService().paginate_entities(query)
    return paginated_cars


@client_owner_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    summary='Update certain fields of existing user car',
)
async def update_user_car(id: int, new_values: schemas.UserCarUpdate):
    updated_user_car = await UserCarService().update_entity(id, new_values)
    return updated_user_car


@client_owner_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_user_car(id: int):
    id_ = await UserCarService().delete_entity(id)
    return {'detail': f'User car successfully deleted with id: {id_}'}


router.include_router(client_router)
router.include_router(client_owner_router)

if config.debug:
    from car_wash.utils.fill_db_with_cars import fill_db

    @router.post('/cars/fill_db_with_cars')
    async def fill_db_with_cars(background_tasks: BackgroundTasks):
        if config.filling_db:
            return 'Database is already filling up'
        background_tasks.add_task(fill_db)
        config.filling_db = True
        return 'Started filling database with cars data'
