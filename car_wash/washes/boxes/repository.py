from car_wash.utils.repository import SQLAlchemyRepository
from car_wash.washes.models import Box


class BoxRepository(SQLAlchemyRepository[Box]):
    model = Box
