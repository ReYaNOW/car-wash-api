from car_wash.cars.repository import CarRepository
from car_wash.utils.service import GenericCRUDService


class CarService(GenericCRUDService):
    repository = CarRepository
