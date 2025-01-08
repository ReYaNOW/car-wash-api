from car_wash.utils.service import GenericCRUDService
from car_wash.washes.additions.repository import CarWashAdditionRepository
from car_wash.washes.additions.schemas import CarWashAdditionRead
from car_wash.washes.models import CarWashAddition


class CarWashAdditionService(GenericCRUDService[CarWashAddition]):
    repository = CarWashAdditionRepository

    def __init__(self):
        super().__init__()
        self.addition_repo: CarWashAdditionRepository = self.repository()

    async def read_by_ids(self, ids: list[int]) -> list[CarWashAdditionRead]:
        additions = await self.addition_repo.find_by_ids(ids)
        return [
            CarWashAdditionRead.model_validate(addition)
            for addition in additions
        ]
