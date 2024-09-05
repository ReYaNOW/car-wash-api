from car_wash.cars.repository import UserCarRepository
from car_wash.cars.schemas import UserCarCreate
from car_wash.users.models import User
from car_wash.utils.service import GenericCRUDService


class UserCarService(GenericCRUDService):
    repository = UserCarRepository

    async def create_user_car(self, user: User, new_car: UserCarCreate) -> int:
        new_car_dict = new_car.model_dump()
        new_car_dict['user_id'] = user.id
        user_car_id = await self.crud_repo.add_one(new_car_dict)
        return user_car_id
