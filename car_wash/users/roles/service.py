from car_wash.users.roles.repository import RoleRepository
from car_wash.utils.service import GenericCRUDService


class RoleService(GenericCRUDService):
    repository = RoleRepository
