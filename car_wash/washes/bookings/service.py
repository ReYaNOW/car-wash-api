from car_wash.users.models import User
from car_wash.utils.service import GenericCRUDService
from car_wash.washes.bookings.repository import BookingRepository
from car_wash.washes.bookings.schemas import BookingCreate


class BookingService(GenericCRUDService):
    repository = BookingRepository

    async def create_booking(
        self, user: User, new_booking: BookingCreate
    ) -> int:
        entity_dict = new_booking.model_dump()
        entity_dict['user_id'] = user.id
        entity_id = await self.crud_repo.add_one(entity_dict)
        return entity_id
