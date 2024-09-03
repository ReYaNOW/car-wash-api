from car_wash.utils.service import GenericCRUDService
from car_wash.washes.schedules.repository import ScheduleRepository


class ScheduleService(GenericCRUDService):
    repository = ScheduleRepository
