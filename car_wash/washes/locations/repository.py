from car_wash.utils.repository import SQLAlchemyRepository
from car_wash.washes.locations.models import CarWashLocation


class CarWashLocationRepository(SQLAlchemyRepository):
    model = CarWashLocation
