from car_wash.cars.models import CarGeneration
from car_wash.utils.repository import SQLAlchemyRepository


class CarGenerationRepository(SQLAlchemyRepository[CarGeneration]):
    model = CarGeneration
