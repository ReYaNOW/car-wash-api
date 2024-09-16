from datetime import date as dt
from datetime import datetime, time
from typing import Protocol

from sqlalchemy import and_, func, or_, select

from car_wash.database import async_session_maker
from car_wash.utils.exception_handling import orm_errors_handler
from car_wash.utils.repository import SQLAlchemyRepository
from car_wash.washes.models import Booking, Box, CarWash, Schedule


class RowProtocol(Protocol):
    box_id: int
    start_time: time
    end_time: time
    start_datetime: datetime | None
    end_datetime: datetime | None
    previous_booking_end: datetime | None


class CarWashRepository(SQLAlchemyRepository[CarWash]):
    model = CarWash
    schedule_model = Schedule
    booking_model = Booking

    @orm_errors_handler
    async def fetch_schedule_and_booking(
        self, car_wash_id: int, date: dt
    ) -> list[RowProtocol]:
        day_of_week = date.weekday()
        start_of_day = datetime.combine(date, time.min)
        end_of_day = datetime.combine(date, time.max)
        async with async_session_maker() as session:
            query = (
                select(
                    Box.id.label('box_id'),
                    Schedule.start_time,
                    Schedule.end_time,
                    Booking.start_datetime,
                    Booking.end_datetime,
                )
                .select_from(Box)
                .join(Schedule, Schedule.car_wash_id == Box.car_wash_id)
                .outerjoin(
                    Booking,
                    and_(
                        Booking.box_id == Box.id,
                        or_(
                            Booking.start_datetime.between(
                                start_of_day, end_of_day
                            ),
                            Booking.end_datetime.between(
                                start_of_day, end_of_day
                            ),
                            and_(
                                Booking.start_datetime <= start_of_day,
                                Booking.end_datetime >= end_of_day,
                            ),
                        ),
                    ),
                )
                .where(
                    Schedule.car_wash_id == car_wash_id,
                    Schedule.day_of_week == day_of_week,
                    Schedule.is_available.is_(True),
                    or_(
                        Booking.id.is_(None),
                        func.coalesce(Booking.is_exception, False).is_(False),
                    ),
                )
                .order_by(Box.id, Booking.start_datetime)
            )

            result = await session.execute(query)
            return result.fetchall()
