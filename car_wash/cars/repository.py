from car_wash.cars.models import Car
from car_wash.utils.repository import SQLAlchemyRepository


class CarRepository(SQLAlchemyRepository):
    model = Car
