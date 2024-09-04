from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.utils.router import get_admin_router, get_client_router
from car_wash.washes.schedules import schemas
from car_wash.washes.schedules.service import ScheduleService

router = APIRouter()

client_router = get_client_router('/schedules', tags=['CarWashes|Schedules'])
admin_router = get_admin_router('/schedules', tags=['CarWashes|Schedules'])


@admin_router.post('', response_model=schemas.CreateResponse)
async def create_schedule(new_schedule: schemas.ScheduleCreate):
    schedule_id = await ScheduleService().create_entity(new_schedule)
    return {'schedule_id': schedule_id}


@client_router.get('/{id}', response_model=schemas.ReadResponse)
async def read_schedule(id: int):
    schedule = await ScheduleService().read_entity(id)
    return schedule


@client_router.get('', response_model=schemas.ListResponse)
async def list_schedules(query: Annotated[schemas.ScheduleList, Depends()]):
    paginated_schedules = await ScheduleService().paginate_entities(query)
    return paginated_schedules


@admin_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    description='Update certain fields of existing schedule',
)
async def update_schedule(id: int, new_values: schemas.ScheduleUpdate):
    updated_schedule = await ScheduleService().update_entity(id, new_values)
    return updated_schedule


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_schedule(id: int):
    id_ = await ScheduleService().delete_entity(id)
    return {'detail': f'Schedule successfully deleted with id: {id_}'}


router.include_router(client_router)
router.include_router(admin_router)
