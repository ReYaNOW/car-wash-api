from car_wash.utils.repository import SQLAlchemyRepository
from car_wash.washes.models import CarWash


class CarWashRepository(SQLAlchemyRepository):
    model = CarWash
