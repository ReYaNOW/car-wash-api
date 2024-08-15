from car_wash.cars.body_types.models import CarBodyType
from car_wash.utils.repository import SQLAlchemyRepository


class CarBodyTypeRepository(SQLAlchemyRepository):
    model = CarBodyType
