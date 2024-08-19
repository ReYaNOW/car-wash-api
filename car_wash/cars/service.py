from car_wash.cars.repository import UserCarRepository
from car_wash.utils.service import GenericCRUDService


class UserCarService(GenericCRUDService):
    repository = UserCarRepository
