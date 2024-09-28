from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends

from car_wash.auth.dependencies import get_user_client
from car_wash.storage.schemas import AnnValidateImage
from car_wash.users import schemas
from car_wash.users.models import User
from car_wash.users.roles.router import router as roles_router
from car_wash.users.service import UserService
from car_wash.utils.routers import (
    get_admin_router,
    get_client_router,
    get_owner_router,
)

router = APIRouter()

router.include_router(roles_router)

client_router = get_client_router('/users', tags=['Users'])
client_owner_router = get_owner_router('/users', UserService, tags=['Users'])
admin_router = get_admin_router('/users', tags=['Users'])


@client_router.get('/me', response_model=schemas.UserReadWithRole)
async def show_logged_user(
    user: Annotated[User, Depends(get_user_client)],
    bg_tasks: BackgroundTasks,
):
    user_with_img_link = await UserService().add_img_link_to_user(
        schemas.UserReadWithRole.model_validate(user), bg_tasks
    )
    return user_with_img_link


@admin_router.post('', response_model=schemas.CreateResponse)
async def create_user(
    new_user: schemas.UserCreate,
    img: AnnValidateImage,
):
    user_id = await UserService().create_user(new_user, img)
    return {'user_id': user_id}


@admin_router.get('/{id}', response_model=schemas.UserReadWithRole)
async def read_user(id: int, bg_tasks: BackgroundTasks):
    user = await UserService().read_user(id, bg_tasks)
    return user


@admin_router.get('', response_model=schemas.ListResponse)
async def list_users(
    query: Annotated[schemas.UserList, Depends()], bg_tasks: BackgroundTasks
):
    users = await UserService().paginate_users(query, bg_tasks)
    return users


@client_owner_router.patch(
    '/{id}',
    response_model=schemas.UserRead,
    summary='Update certain fields of existing user',
)
async def update_user(
    id: int,
    new_values: schemas.UserUpdate,
    img: AnnValidateImage,
    bg_tasks: BackgroundTasks,
):
    updated_user = await UserService().update_user(
        id, new_values, img, bg_tasks
    )
    return updated_user


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_user(id: int):
    await UserService().delete_user(id)
    return {'detail': f'User successfully deleted with id: {id}'}


router.include_router(client_router)
router.include_router(client_owner_router)
router.include_router(admin_router)
