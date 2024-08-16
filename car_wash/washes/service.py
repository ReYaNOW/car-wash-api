from car_wash.utils.service import GenericCRUDService
from car_wash.washes.repository import CarWashRepository


class CarWashService(GenericCRUDService):
    repository = CarWashRepository
