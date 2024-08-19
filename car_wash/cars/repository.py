from car_wash.cars.models import UserCar
from car_wash.utils.repository import SQLAlchemyRepository


class UserCarRepository(SQLAlchemyRepository):
    model = UserCar
