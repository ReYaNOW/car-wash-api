from car_wash.users.repository import UsersRepository
from car_wash.utils.service import GenericCRUDService


class UsersService(GenericCRUDService):
    repository = UsersRepository
