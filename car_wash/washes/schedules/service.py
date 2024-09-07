from car_wash.utils.service import GenericCRUDService
from car_wash.washes.models import Schedule
from car_wash.washes.schedules.repository import ScheduleRepository


class ScheduleService(GenericCRUDService[Schedule]):
    repository = ScheduleRepository
