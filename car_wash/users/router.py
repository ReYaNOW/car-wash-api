from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.auth.dependencies import get_user_admin, get_user_client
from car_wash.users import schemas
from car_wash.users.models import User
from car_wash.users.roles.router import router as roles_router
from car_wash.users.service import UserService

router = APIRouter(tags=['Users'])

router.include_router(roles_router)

client_router = APIRouter(
    prefix='/users', dependencies=[Depends(get_user_client)]
)
admin_router = APIRouter(
    prefix='/users', dependencies=[Depends(get_user_admin)]
)


@client_router.post('/me', response_model=schemas.UserRead)
async def show_logged_user(user: Annotated[User, Depends(get_user_client)]):
    return user


@admin_router.post('', response_model=schemas.CreateResponse)
async def create_user(new_user: schemas.UserCreate):
    user_id = await UserService().create_entity(new_user)
    return {'user_id': user_id}


@admin_router.get('/{id}', response_model=schemas.ReadResponse)
async def read_user(id: int):
    user = await UserService().read_entity(id)
    return user


@admin_router.get('', response_model=schemas.ListResponse)
async def list_users(query: Annotated[schemas.UserList, Depends()]):
    users = await UserService().paginate_entities(query)
    return users


@admin_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    description='Update certain fields of existing user',
)
async def update_user(id: int, new_values: schemas.UserUpdate):
    updated_user = await UserService().update_entity(id, new_values)
    return updated_user


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_user(id: int):
    await UserService().delete_entity(id)
    return {'detail': f'User successfully deleted with id: {id}'}


router.include_router(client_router)
router.include_router(admin_router)
