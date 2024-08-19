from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.users import schemas
from car_wash.users.service import UsersService

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('', response_model=schemas.CreateResponse)
async def create_user(new_user: schemas.UserCreate):
    user_id = await UsersService().create_entity(new_user)
    return {'user_id': user_id}


@router.get('/{id}', response_model=schemas.ReadResponse)
async def read_user(id: int):
    user = await UsersService().read_entity(id)
    return user


@router.get('', response_model=list[schemas.ReadResponse])
async def list_users(query: Annotated[schemas.UserList, Depends()]):
    users = await UsersService().paginate_entities(query)
    return users


@router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    description='Update certain fields of existing user',
)
async def update_user(id: int, new_values: schemas.UserUpdate):
    updated_user = await UsersService().update_entity(id, new_values)
    return updated_user


@router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_user(id: int):
    await UsersService().delete_entity(id)
    return {'detail': f'User successfully deleted with id: {id}'}
