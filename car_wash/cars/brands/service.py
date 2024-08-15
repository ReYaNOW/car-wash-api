from car_wash.cars.brands.repository import CarBrandRepository
from car_wash.utils.service import GenericCRUDService


class CarBrandService(GenericCRUDService):
    repository = CarBrandRepository
