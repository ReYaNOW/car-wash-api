from car_wash.users.models import Role
from car_wash.utils.repository import SQLAlchemyRepository


class RoleRepository(SQLAlchemyRepository):
    model = Role
