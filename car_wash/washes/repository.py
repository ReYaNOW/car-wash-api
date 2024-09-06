from datetime import date as date_type
from datetime import datetime, time

from sqlalchemy import select

from car_wash.database import async_session_maker
from car_wash.utils.exception_handling import orm_errors_handler
from car_wash.utils.repository import SQLAlchemyRepository
from car_wash.washes.models import Booking, CarWash, Schedule


class CarWashRepository(SQLAlchemyRepository):
    model = CarWash
    schedule_model = Schedule
    booking_model = Booking

    @orm_errors_handler
    async def find_available_times(
        self, car_wash_id: int, date: date_type
    ) -> list[tuple[datetime, datetime]]:
        day_of_week = date.weekday()

        booking_model = self.booking_model
        schedule_model = self.schedule_model

        async with async_session_maker() as session:
            schedule_query = select(schedule_model).where(
                schedule_model.car_wash_id == car_wash_id,
                schedule_model.day_of_week == day_of_week,
                schedule_model.is_available.is_(True),
            )
            schedule_result = await session.execute(schedule_query)
            schedule = schedule_result.scalar()

            if not schedule:
                return []

            day_start = datetime.combine(date, time.min)
            day_end = datetime.combine(date, time.max)

            bookings_query = (
                select(booking_model)
                .where(
                    booking_model.car_wash_id == car_wash_id,
                    booking_model.start_datetime >= day_start,
                    booking_model.end_datetime <= day_end,
                    booking_model.is_exception.is_(False),
                )
                .order_by(booking_model.start_datetime)
            )
            bookings_result = await session.execute(bookings_query)
            bookings: list[booking_model] = bookings_result.scalars().all()

        available_start = datetime.combine(date, schedule.start_time)
        available_end = datetime.combine(date, schedule.end_time)

        available_slots = []

        if not bookings:
            available_slots.append((available_start, available_end))
            return available_slots

        current_start = available_start

        for booking in bookings:
            if booking.start_datetime > current_start:
                available_slots.append((current_start, booking.start_datetime))

            current_start = booking.end_datetime

        if current_start < available_end:
            available_slots.append((current_start, available_end))

        return available_slots
