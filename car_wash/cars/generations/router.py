from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.cars.generations import schemas
from car_wash.cars.generations.service import CarGenerationService

router = APIRouter(prefix='/generations')


@router.post('', response_model=schemas.CreateResponse)
async def create_generation(new_generation: schemas.GenerationCreate):
    generation_id = await CarGenerationService().create_entity(new_generation)
    return {'generation_id': generation_id}


@router.get('/{id}', response_model=schemas.ReadResponse)
async def read_generation(id: int):
    generation = await CarGenerationService().read_entity(id)
    return generation


@router.get('', response_model=list[schemas.ReadResponse])
async def list_generations(
    query: Annotated[schemas.GenerationList, Depends()],
):
    generations = await CarGenerationService().list_entities(query)
    return generations


@router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    description='Update certain fields of existing generation',
)
async def update_generation(id: int, new_values: schemas.GenerationUpdate):
    updated_generation = await CarGenerationService().update_entity(
        id, new_values
    )
    return updated_generation


@router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_generation(id: int):
    id_ = await CarGenerationService().delete_entity(id)
    return {'detail': f'Generation successfully deleted with id: {id_}'}