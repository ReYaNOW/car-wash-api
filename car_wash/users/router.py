from fastapi import APIRouter

from car_wash.users.repository import UsersRepository
from car_wash.users.schemas import (
    CreateResponse,
    DeleteResponse,
    ReadResponse,
    UpdateResponse,
    UserCreate,
    UserUpdate,
)

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('', response_model=CreateResponse)
async def create_user(new_user: UserCreate):
    user_dict = new_user.model_dump()
    user_id = await UsersRepository().add_one(user_dict)
    return {'user_id': user_id}


@router.get('/{id}', response_model=ReadResponse)
async def read_user(id: int):
    user = await UsersRepository().find_one(id)
    return user


@router.get('', response_model=list[ReadResponse])
async def list_users(page: int, limit: int = 10):
    users = await UsersRepository().find_many(page, limit)
    return users


@router.patch(
    '/{id}',
    response_model=UpdateResponse,
    description='Update certain fields of existing user',
)
async def update_user(id: int, new_values: UserUpdate):
    new_values_dict = new_values.model_dump(exclude_none=True)
    updated_user = await UsersRepository().change_one(id, new_values_dict)
    return updated_user


@router.delete('/{id}', response_model=DeleteResponse)
async def delete_user(id: int):
    await UsersRepository().delete_one(id)
    return {'detail': f'User successfully deleted with id: {id}'}
