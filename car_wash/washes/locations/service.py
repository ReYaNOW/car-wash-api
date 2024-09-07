from car_wash.utils.service import GenericCRUDService
from car_wash.washes.locations.models import CarWashLocation
from car_wash.washes.locations.repository import CarWashLocationRepository


class CarWashLocationService(GenericCRUDService[CarWashLocation]):
    repository = CarWashLocationRepository
