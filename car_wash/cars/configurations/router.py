from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.cars.configurations import schemas
from car_wash.cars.configurations.service import CarConfigurationService
from car_wash.utils.routers import get_admin_router, get_client_router

router = APIRouter()

client_router = get_client_router(
    '/configurations', tags=['Cars|Configuration']
)
admin_router = get_admin_router('/configurations', tags=['Cars|Configuration'])


@admin_router.post('', response_model=schemas.CreateResponse)
async def create_configuration(new_configuration: schemas.ConfigurationCreate):
    configuration_id = await CarConfigurationService().create_entity(
        new_configuration
    )
    return {'configuration_id': configuration_id}


@client_router.get('/{id}', response_model=schemas.ReadResponse)
async def read_configuration(id: int):
    configuration = await CarConfigurationService().read_entity(id)
    return configuration


@client_router.get('', response_model=schemas.ListResponse)
async def list_configurations(
    query: Annotated[schemas.ConfigurationList, Depends()],
):
    paginated_configurations = (
        await CarConfigurationService().paginate_entities(query)
    )
    return paginated_configurations


@admin_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    summary='Update certain fields of existing configuration',
)
async def update_configuration(
    id: int, new_values: schemas.ConfigurationUpdate
):
    updated_configuration = await CarConfigurationService().update_entity(
        id, new_values
    )
    return updated_configuration


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_configuration(id: int):
    id_ = await CarConfigurationService().delete_entity(id)
    return {'detail': f'Configuration successfully deleted with id: {id_}'}


router.include_router(admin_router)
router.include_router(client_router)
