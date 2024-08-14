from car_wash.users.models import Users
from car_wash.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = Users
