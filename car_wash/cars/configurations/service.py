from car_wash.cars.configurations.repository import CarConfigurationRepository
from car_wash.cars.models import CarConfiguration
from car_wash.utils.service import GenericCRUDService


class CarConfigurationService(GenericCRUDService[CarConfiguration]):
    repository = CarConfigurationRepository
