from car_wash.cars.body_types.repository import CarBodyTypeRepository
from car_wash.cars.models import CarBodyType
from car_wash.utils.service import GenericCRUDService


class CarBodyTypeService(GenericCRUDService[CarBodyType]):
    repository = CarBodyTypeRepository
