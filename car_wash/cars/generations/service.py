from car_wash.cars.generations.repository import CarGenerationRepository
from car_wash.utils.service import GenericCRUDService


class CarGenerationService(GenericCRUDService):
    repository = CarGenerationRepository
