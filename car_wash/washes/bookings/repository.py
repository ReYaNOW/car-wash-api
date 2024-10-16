from sqlalchemy import BinaryExpression, and_, select

from car_wash.database import async_session_maker
from car_wash.utils.exception_handling import orm_errors_handler
from car_wash.utils.repository import SQLAlchemyRepository
from car_wash.washes.models import Booking, Box


class BookingRepository(SQLAlchemyRepository[Booking]):
    model = Booking

    @orm_errors_handler
    async def find_many(
        self,
        page: int,
        limit: int,
        order_by: str,
        filters: dict | list[BinaryExpression],
        relationships: list | None = None,
    ) -> list[Booking]:
        offset_value = page * limit - limit
        async with async_session_maker() as session:
            query = (
                select(self.model)
                .offset(offset_value)
                .limit(limit)
                .order_by(order_by)
            )

            if 'car_wash_id' in filters:
                query = query.join(self.model.box).where(
                    Box.car_wash_id == filters.pop('car_wash_id')
                )

            if filters:
                expressions = self.get_expressions(filters)
                query = query.where(and_(*expressions))

            query = self.add_joined_loads(query, relationships)

            res = await session.execute(query)
            return res.unique().scalars().all()
