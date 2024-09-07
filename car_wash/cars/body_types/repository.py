from car_wash.cars.models import CarBodyType
from car_wash.utils.repository import SQLAlchemyRepository


class CarBodyTypeRepository(SQLAlchemyRepository[CarBodyType]):
    model = CarBodyType
