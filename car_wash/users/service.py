from typing import Literal

from car_wash.auth.exceptions import credentials_exc
from car_wash.auth.schemas import UserCredentials, UserForDB, UserInDB
from car_wash.auth.utils import PasswordService
from car_wash.users.exceptions import NoDefaultRoleError
from car_wash.users.repository import UserRepository
from car_wash.users.roles.repository import RoleRepository
from car_wash.users.schemas import UserRegistration
from car_wash.utils.repository import AnyModel
from car_wash.utils.service import GenericCRUDService


class UserService(GenericCRUDService):
    repository = UserRepository

    user_repo = UserRepository
    role_repo = RoleRepository
    password_service = PasswordService

    def __init__(self):
        super().__init__()
        self.user_repo = self.user_repo()
        self.role_repo = self.role_repo()
        self.password_service = self.password_service()

    async def create_user(self, new_user: UserRegistration) -> int:
        default_role = await self.find_default_role()

        user_dict = new_user.model_dump()
        hashed_pass = await self.password_service.a_get_pass_hash(
            new_user.password
        )
        user_for_db = UserForDB(
            **user_dict, hashed_password=hashed_pass, role_id=default_role.id
        )
        user_id = await self.user_repo.add_one(user_for_db.model_dump())
        return user_id

    async def authenticate_user(
        self,
        user_credentials: UserCredentials,
        auth_by: Literal['id', 'username_and_pass'],
    ) -> UserInDB:
        if auth_by == 'id':
            user = await self.read_user_with_role(user_credentials.id)
            return UserInDB.model_validate(user)

        user = await self.read_user_by_name(user_credentials.username)

        if not user or not await self.password_service.a_verify_pass(
            user_credentials.password, user.hashed_password
        ):
            raise credentials_exc
        return UserInDB.model_validate(user)

    async def get_user_by_id(self, user_id: int) -> AnyModel:
        user = await self.user_repo.find_one(user_id)
        if not user:
            raise credentials_exc
        return user

    async def read_user_by_name(self, username: str) -> AnyModel:
        return await self.user_repo.find_one_by_custom_field(
            'username', username
        )

    async def read_user_with_role(self, id: int) -> AnyModel:
        return await self.user_repo.find_one(id, [self.user_repo.model.role])

    async def find_default_role(self) -> AnyModel:
        default_role = await self.role_repo.find_one_by_custom_field(
            'name', 'client'
        )
        if not default_role:
            raise NoDefaultRoleError

        return default_role


async def get_user_service() -> UserService:
    return UserService()
