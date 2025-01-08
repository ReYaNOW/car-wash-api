from sqlalchemy import select

from car_wash.database import async_session_maker
from car_wash.utils.exception_handling import orm_errors_handler
from car_wash.utils.repository import SQLAlchemyRepository
from car_wash.washes.models import CarWashAddition


class CarWashAdditionRepository(SQLAlchemyRepository[CarWashAddition]):
    model = CarWashAddition

    @orm_errors_handler
    async def find_by_ids(self, ids: list[int]) -> list[CarWashAddition]:
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id.in_(ids))

            res = await session.execute(query)
            return res.scalars().all()
