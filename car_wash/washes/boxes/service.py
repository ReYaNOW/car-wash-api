from car_wash.utils.service import GenericCRUDService
from car_wash.washes.boxes.repository import BoxRepository
from car_wash.washes.models import Box


class BoxService(GenericCRUDService[Box]):
    repository = BoxRepository
