from car_wash.cars.models import CarModel
from car_wash.utils.repository import SQLAlchemyRepository


class CarModelRepository(SQLAlchemyRepository):
    model = CarModel
