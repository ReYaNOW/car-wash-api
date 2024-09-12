from car_wash.users.models import User
from car_wash.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):
    model = User
