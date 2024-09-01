from car_wash.users.repository import UserRepository
from car_wash.utils.service import GenericCRUDService


class UserService(GenericCRUDService):
    repository = UserRepository
