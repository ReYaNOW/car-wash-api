from car_wash.utils.service import GenericCRUDService
from car_wash.washes.locations.repository import CarWashLocationRepository


class CarWashLocationService(GenericCRUDService):
    repository = CarWashLocationRepository
