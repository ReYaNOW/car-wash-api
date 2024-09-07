from car_wash.cars.car_models.repository import CarModelRepository
from car_wash.cars.models import CarModel
from car_wash.utils.service import GenericCRUDService


class CarModelService(GenericCRUDService[CarModel]):
    repository = CarModelRepository
