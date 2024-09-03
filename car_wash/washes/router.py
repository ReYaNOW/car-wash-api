import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.auth.dependencies import get_user_admin, get_user_client
from car_wash.washes import schemas
from car_wash.washes.bookings.router import router as bookings_router
from car_wash.washes.locations.router import router as locations_router
from car_wash.washes.schedules.router import router as schedules_router
from car_wash.washes.service import CarWashService

router = APIRouter(tags=['CarWashes'])

sub_router = APIRouter(
    prefix='/car_washes',
    tags=['CarWashBookings, CarWashSchedules, CarWashLocations'],
)
sub_router.include_router(bookings_router)
sub_router.include_router(schedules_router)
sub_router.include_router(locations_router)

client_router = APIRouter(
    prefix='/car_washes', dependencies=[Depends(get_user_client)]
)
admin_router = APIRouter(
    prefix='/car_washes', dependencies=[Depends(get_user_admin)]
)


@admin_router.post('', response_model=schemas.CreateResponse)
async def create_car_wash(new_car_wash: schemas.CarWashCreate):
    car_wash_id = await CarWashService().create_entity(new_car_wash)
    return {'car_wash_id': car_wash_id}


@client_router.get('/{id}', response_model=schemas.ReadResponse)
async def read_car_wash(id: int):
    car_wash = await CarWashService().read_entity(id)
    return car_wash


@client_router.get('', response_model=schemas.ListResponse)
async def list_car_washes(query: Annotated[schemas.CarWashList, Depends()]):
    car_washes = await CarWashService().paginate_entities(query)
    return car_washes


@admin_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    description='Update certain fields of existing car wash',
)
async def update_car_wash(id: int, new_values: schemas.CarWashUpdate):
    updated_car_wash = await CarWashService().update_entity(id, new_values)
    return updated_car_wash


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_car_wash(id: int):
    id_ = await CarWashService().delete_entity(id)
    return {'detail': f'Car wash successfully deleted with id: {id_}'}


@client_router.get(
    '/{id}/available_times', response_model=schemas.AvailableTimesResponse
)
async def get_available_times(id: int, date: datetime.date):
    available_times = await CarWashService().get_available_times(id, date)
    print(available_times[0])
    return {'available_times': available_times}


router.include_router(client_router)
router.include_router(admin_router)
