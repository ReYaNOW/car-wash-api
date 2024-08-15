from car_wash.cars.brands.models import CarBrand
from car_wash.utils.repository import SQLAlchemyRepository


class CarBrandRepository(SQLAlchemyRepository):
    model = CarBrand
