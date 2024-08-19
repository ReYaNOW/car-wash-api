from car_wash.cars.models import CarConfiguration
from car_wash.utils.repository import SQLAlchemyRepository


class CarConfigurationRepository(SQLAlchemyRepository):
    model = CarConfiguration
