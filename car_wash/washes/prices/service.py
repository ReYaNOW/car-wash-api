from car_wash.utils.service import GenericCRUDService
from car_wash.washes.models import CarWashPrice
from car_wash.washes.prices.repository import CarWashPriceRepository


class CarWashPriceService(GenericCRUDService[CarWashPrice]):
    repository = CarWashPriceRepository
