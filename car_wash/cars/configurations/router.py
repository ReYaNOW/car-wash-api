from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.cars.configurations import schemas
from car_wash.cars.configurations.service import CarConfigurationService

router = APIRouter(prefix='/configurations')


@router.post('', response_model=schemas.CreateResponse)
async def create_configuration(new_configuration: schemas.ConfigurationCreate):
    configuration_id = await CarConfigurationService().create_entity(
        new_configuration
    )
    return {'configuration_id': configuration_id}


@router.get('/{id}', response_model=schemas.ReadResponse)
async def read_configuration(id: int):
    configuration = await CarConfigurationService().read_entity(id)
    return configuration


@router.get('', response_model=list[schemas.ReadResponse])
async def list_configurations(
    query: Annotated[schemas.ConfigurationList, Depends()],
):
    configurations = await CarConfigurationService().list_entities(query)
    return configurations


@router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    description='Update certain fields of existing configuration',
)
async def update_configuration(
    id: int, new_values: schemas.ConfigurationUpdate
):
    updated_configuration = await CarConfigurationService().update_entity(
        id, new_values
    )
    return updated_configuration


@router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_configuration(id: int):
    id_ = await CarConfigurationService().delete_entity(id)
    return {'detail': f'Configuration successfully deleted with id: {id_}'}
