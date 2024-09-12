from car_wash.utils.repository import SQLAlchemyRepository
from car_wash.washes.models import Schedule


class ScheduleRepository(SQLAlchemyRepository[Schedule]):
    model = Schedule
