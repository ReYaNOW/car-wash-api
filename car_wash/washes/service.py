import datetime

from car_wash.utils.service import GenericCRUDService
from car_wash.washes.repository import CarWashRepository


class CarWashService(GenericCRUDService):
    repository = CarWashRepository
    crud_repo: CarWashRepository

    async def get_available_times(self, car_wash_id: int, date: datetime.date):
        return await self.crud_repo.find_available_times(car_wash_id, date)
