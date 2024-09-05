from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.users.roles import schemas
from car_wash.users.roles.service import RoleService
from car_wash.utils.routers import get_admin_router, get_client_router

router = APIRouter()

client_router = get_client_router('/roles', tags=['Users|Roles'])
admin_router = get_admin_router('/roles', tags=['Users|Roles'])


@admin_router.post('', response_model=schemas.CreateResponse)
async def create_role(new_role: schemas.RoleCreate):
    role_id = await RoleService().create_entity(new_role)
    return {'role_id': role_id}


@client_router.get('/{id}', response_model=schemas.ReadResponse)
async def read_role(id: int):
    role = await RoleService().read_entity(id)
    return role


@client_router.get('', response_model=schemas.ListResponse)
async def list_roles(query: Annotated[schemas.RoleList, Depends()]):
    paginated_roles = await RoleService().paginate_entities(query)
    return paginated_roles


@admin_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    summary='Update certain fields of existing role',
)
async def update_role(id: int, new_values: schemas.RoleUpdate):
    updated_role = await RoleService().update_entity(id, new_values)
    return updated_role


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_role(id: int):
    id_ = await RoleService().delete_entity(id)
    return {'detail': f'role successfully deleted with id: {id_}'}


router.include_router(admin_router)
router.include_router(client_router)
