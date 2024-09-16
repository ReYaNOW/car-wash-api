from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.utils.routers import get_admin_router, get_client_router
from car_wash.washes.boxes import schemas
from car_wash.washes.boxes.service import BoxService

router = APIRouter()

client_router = get_client_router('/boxes', tags=['CarWashes|Boxes'])
admin_router = get_admin_router('/boxes', tags=['CarWashes|Boxes'])


@admin_router.post('', response_model=schemas.CreateResponse)
async def create_box(new_boxes: schemas.BoxCreate):
    box_id = await BoxService().create_entity(new_boxes)
    return {'box_id': box_id}


@client_router.get('/{id}', response_model=schemas.ReadResponse)
async def read_box(id: int):
    box = await BoxService().read_entity(id)
    return box


@client_router.get('', response_model=schemas.ListResponse)
async def list_boxes(
    query: Annotated[schemas.BoxList, Depends()],
):
    boxes = await BoxService().paginate_entities(query)
    return boxes


@admin_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    summary='Update certain fields of existing box',
)
async def update_box(id: int, new_values: schemas.BoxUpdate):
    updated_box = await BoxService().update_entity(id, new_values)
    return updated_box


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_box(id: int):
    id_ = await BoxService().delete_entity(id)
    return {'detail': f'Box successfully deleted with id: {id_}'}


router.include_router(admin_router)
router.include_router(client_router)
