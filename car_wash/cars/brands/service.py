from car_wash.cars.brands.repository import CarBrandRepository
from car_wash.cars.models import CarBrand
from car_wash.utils.service import GenericCRUDService


class CarBrandService(GenericCRUDService[CarBrand]):
    repository = CarBrandRepository
