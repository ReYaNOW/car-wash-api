from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.cars.generations import schemas
from car_wash.cars.generations.service import CarGenerationService
from car_wash.utils.router import get_admin_router, get_client_router

router = APIRouter()

client_router = get_client_router('/generations', tags=['Cars|Generations'])
admin_router = get_admin_router('/generations', tags=['Cars|Generations'])


@admin_router.post('', response_model=schemas.CreateResponse)
async def create_generation(new_generation: schemas.GenerationCreate):
    generation_id = await CarGenerationService().create_entity(new_generation)
    return {'generation_id': generation_id}


@client_router.get('/{id}', response_model=schemas.ReadResponse)
async def read_generation(id: int):
    generation = await CarGenerationService().read_entity(id)
    return generation


@client_router.get('', response_model=schemas.ListResponse)
async def list_generations(
    query: Annotated[schemas.GenerationList, Depends()],
):
    paginated_generations = await CarGenerationService().paginate_entities(
        query
    )
    return paginated_generations


@admin_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    summary='Update certain fields of existing generation',
)
async def update_generation(id: int, new_values: schemas.GenerationUpdate):
    updated_generation = await CarGenerationService().update_entity(
        id, new_values
    )
    return updated_generation


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_generation(id: int):
    id_ = await CarGenerationService().delete_entity(id)
    return {'detail': f'Generation successfully deleted with id: {id_}'}


router.include_router(admin_router)
router.include_router(client_router)
