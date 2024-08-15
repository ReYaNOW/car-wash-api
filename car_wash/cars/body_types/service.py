from car_wash.cars.body_types.repository import CarBodyTypeRepository
from car_wash.utils.service import GenericCRUDService


class CarBodyTypeService(GenericCRUDService):
    repository = CarBodyTypeRepository
