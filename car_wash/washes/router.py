import datetime
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends

from car_wash.storage.schemas import AnnValidateImage
from car_wash.utils.routers import get_admin_router, get_client_router
from car_wash.washes import schemas
from car_wash.washes.bookings.router import router as bookings_router
from car_wash.washes.boxes.router import router as boxes_router
from car_wash.washes.locations.router import router as locations_router
from car_wash.washes.prices.router import router as prices_router
from car_wash.washes.schedules.router import router as schedules_router
from car_wash.washes.service import CarWashService

router = APIRouter()

sub_router = APIRouter(prefix='/car_washes')

sub_router.include_router(locations_router)
sub_router.include_router(schedules_router)
sub_router.include_router(boxes_router)
sub_router.include_router(bookings_router)
sub_router.include_router(prices_router)


client_router = get_client_router('/car_washes', tags=['CarWashes'])
admin_router = get_admin_router('/car_washes', tags=['CarWashes'])


@admin_router.post('', response_model=schemas.CreateResponse)
async def create_car_wash(
    new_car_wash: schemas.CarWashCreate, img: AnnValidateImage
):
    car_wash_id = await CarWashService().create_car_wash(new_car_wash, img)
    return {'car_wash_id': car_wash_id}


@client_router.get('/{id}', response_model=schemas.CarWashRead)
async def read_car_wash(id: int, bg_tasks: BackgroundTasks):
    car_wash = await CarWashService().read_car_wash(id, bg_tasks)
    return car_wash


@client_router.get('', response_model=schemas.ListResponse)
async def list_car_washes(
    query: Annotated[schemas.CarWashList, Depends()], bg_tasks: BackgroundTasks
):
    car_washes = await CarWashService().paginate_car_washes(query, bg_tasks)
    return car_washes


@admin_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    summary='Update certain fields of existing car wash',
)
async def update_car_wash(
    id: int,
    new_values: schemas.CarWashUpdate,
    img: AnnValidateImage,
    bg_tasks: BackgroundTasks,
):
    updated_car_wash = await CarWashService().update_car_wash(
        id, new_values, img, bg_tasks
    )
    return updated_car_wash


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_car_wash(id: int):
    await CarWashService().delete_car_wash(id)
    return {'detail': f'Car wash successfully deleted with id: {id}'}


@client_router.get(
    '/{id}/available_times', response_model=schemas.AvailableTimesResponse
)
async def get_available_times(id: int, date: datetime.date):
    available_times = await CarWashService().get_available_times(id, date)
    return {'available_times': available_times}


@client_router.get('/{id}/show', response_model=schemas.ShowHideResponse)
async def show_car_wash(id: int):
    await CarWashService().show_car_wash(id)
    return {'status': 'This car wash is now showing'}


@client_router.get('/{id}/hide', response_model=schemas.ShowHideResponse)
async def hide_car_wash(id: int):
    await CarWashService().hide_car_wash(id)
    return {'status': 'This car wash is now hidden'}


router.include_router(admin_router)
router.include_router(client_router)
