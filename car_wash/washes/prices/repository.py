from sqlalchemy import select

from car_wash.database import async_session_maker
from car_wash.utils.repository import SQLAlchemyRepository
from car_wash.washes.models import CarWashPrice


class CarWashPriceRepository(SQLAlchemyRepository[CarWashPrice]):
    model = CarWashPrice

    async def select_body_types_from_price(
        self, car_wash_id: int
    ) -> list[int]:
        async with async_session_maker() as session:
            query = select(self.model.body_type_id).where(
                self.model.car_wash_id == car_wash_id
            )

            res = await session.execute(query)
            return res.scalars().all()
