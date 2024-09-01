from car_wash.cars.repository import UserCarRepository
from car_wash.cars.schemas import UserCarCreate, UserCarCreateWithID
from car_wash.users.models import User
from car_wash.utils.service import GenericCRUDService


class UserCarService(GenericCRUDService):
    repository = UserCarRepository

    async def create_user_car(self, user: User, new_car: UserCarCreate):
        new_car_with_id = UserCarCreateWithID(
            **new_car.model_dump(), user_id=user.id
        )
        user_car_id = await UserCarService().create_entity(new_car_with_id)
        return user_car_id
