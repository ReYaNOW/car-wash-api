from sqlalchemy import select

from car_wash.cars.models import CarBodyType
from car_wash.database import async_session_maker
from car_wash.utils.repository import SQLAlchemyRepository


class CarBodyTypeRepository(SQLAlchemyRepository[CarBodyType]):
    model = CarBodyType

    async def find_necessary_bts(self) -> list[CarBodyType]:
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.parent_id.is_(None))

            res = await session.execute(query)
            return res.scalars().all()

    async def find_necessary_bts_ids(self) -> list[int]:
        async with async_session_maker() as session:
            query = select(self.model.id).where(self.model.parent_id.is_(None))

            res = await session.execute(query)
            return res.scalars().all()
