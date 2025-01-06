from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.utils.routers import (
    get_admin_router,
    get_client_router,
    get_owner_router,
)
from car_wash.washes.bookings import schemas
from car_wash.washes.bookings.service import BookingService

router = APIRouter()

client_router = get_client_router('/bookings', tags=['CarWashes|Bookings'])
client_owner_router = get_owner_router(
    '/bookings', BookingService, tags=['CarWashes|Bookings']
)
admin_router = get_admin_router('/prices', tags=['CarWashes|Bookings'])


@client_router.post('', response_model=schemas.CreateResponse)
async def create_booking(new_booking: schemas.BookingCreate):
    booking_id = await BookingService().create_booking(new_booking)
    return {'booking_id': booking_id}


@client_router.get('/{id}', response_model=schemas.ReadResponse)
async def read_booking(id: int):
    booking = await BookingService().read_entity(id)
    return booking


@client_router.get('', response_model=schemas.ListResponse)
async def list_bookings(query: Annotated[schemas.BookingList, Depends()]):
    paginated_bookings = await BookingService().paginate_entities(query)
    return paginated_bookings


@admin_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    summary='Update certain fields of existing booking',
)
async def update_booking(id: int, new_values: schemas.BookingUpdate):
    updated_booking = await BookingService().update_entity(id, new_values)
    return updated_booking


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_booking(id: int):
    id_ = await BookingService().delete_entity(id)
    return {'detail': f'booking successfully deleted with id: {id_}'}


router.include_router(client_router)
router.include_router(client_owner_router)
router.include_router(admin_router)
