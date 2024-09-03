from car_wash.utils.repository import SQLAlchemyRepository
from car_wash.washes.models import Booking


class BookingRepository(SQLAlchemyRepository):
    model = Booking
