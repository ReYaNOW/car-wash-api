from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.cars.car_models import schemas
from car_wash.cars.car_models.service import CarModelService

router = APIRouter(prefix='/models')


@router.post('', response_model=schemas.CreateResponse)
async def create_model(new_model: schemas.ModelCreate):
    model_id = await CarModelService().create_entity(new_model)
    return {'model_id': model_id}


@router.get('/{id}', response_model=schemas.ReadResponse)
async def read_model(id: int):
    model = await CarModelService().read_entity(id)
    return model


@router.get('', response_model=schemas.ListResponse)
async def list_models(query: Annotated[schemas.ModelList, Depends()]):
    paginated_models = await CarModelService().paginate_entities(query)
    return paginated_models


@router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    description='Update certain fields of existing model',
)
async def update_model(id: int, new_values: schemas.ModelUpdate):
    updated_model = await CarModelService().update_entity(id, new_values)
    return updated_model


@router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_model(id: int):
    id_ = await CarModelService().delete_entity(id)
    return {'detail': f'Model successfully deleted with id: {id_}'}
