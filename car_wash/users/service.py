import asyncio
from typing import Annotated, Literal

from fastapi import BackgroundTasks, Depends, UploadFile
from pydantic import HttpUrl

from car_wash.auth.exceptions import CredentialsExc
from car_wash.auth.schemas import UserCredentials, UserWithPass
from car_wash.auth.utils import PasswordService
from car_wash.storage.schemas import S3Folders
from car_wash.storage.service import S3Service
from car_wash.storage.utils import validate_link
from car_wash.users.exceptions import NoDefaultRoleError
from car_wash.users.models import Role, User
from car_wash.users.repository import UserRepository
from car_wash.users.roles.repository import RoleRepository
from car_wash.users.schemas import (
    UserCreate,
    UserList,
    UserRead,
    UserReadWithRole,
    UserRegistration,
    UserUpdate,
)
from car_wash.utils.schemas import GenericListResponse
from car_wash.utils.service import GenericCRUDService


class UserService(GenericCRUDService[User]):
    repository = UserRepository

    user_repo = UserRepository
    role_repo = RoleRepository
    password_service = PasswordService

    def __init__(self):
        super().__init__()
        self.user_repo = self.crud_repo
        self.role_repo = self.role_repo()
        self.s3_service = S3Service()
        self.password_service = self.password_service()

    async def create_user(
        self,
        new_user: UserCreate | UserRegistration,
        avatar: UploadFile | None,
    ) -> int:
        if not new_user.role_id:
            default_role = await self.find_default_role()
            new_user.role_id = default_role.id

        hashed_pass = await self.password_service.a_get_pass_hash(
            new_user.password
        )
        new_user.hashed_password = hashed_pass

        if avatar:
            unique_filename = await self.s3_service.upload_file(
                S3Folders.AVATARS, avatar
            )
            new_user.image_path = unique_filename

        user_id = await self.user_repo.add_one(new_user.model_dump())
        return user_id

    async def authenticate_user(
        self,
        user_credentials: UserCredentials,
        auth_by: Literal['id', 'username_and_pass'],
    ) -> UserWithPass:
        if auth_by == 'id':
            user = await self.read_user_with_role(user_credentials.id)
            return UserWithPass.model_validate(user)

        user = await self.read_user_by_name(user_credentials.username)

        if not user or not await self.password_service.a_verify_pass(
            user_credentials.password, user.hashed_password
        ):
            raise CredentialsExc
        return UserWithPass.model_validate(user)

    async def read_user(
        self, id_: int, bg_tasks: BackgroundTasks
    ) -> UserRead | UserReadWithRole:
        user = await self.user_repo.find_one(id_, relationships=[User.role])
        return await self.add_img_link_to_user(
            UserReadWithRole.model_validate(user), bg_tasks
        )

    async def paginate_users(
        self, query: UserList, bg_tasks: BackgroundTasks
    ) -> GenericListResponse:
        list_response = await self.paginate_entities(query)

        tasks = [
            self.add_img_link_to_user(UserRead.model_validate(user), bg_tasks)
            for user in list_response.data
        ]

        res = await asyncio.gather(*tasks)
        list_response.data = res

        return list_response

    async def add_img_link_to_user(
        self,
        user: User | UserRead | UserReadWithRole,
        bg_tasks: BackgroundTasks,
    ) -> UserRead | UserReadWithRole:
        img_link = user.image_link

        if user.image_path and (
            not img_link or not validate_link(img_link, user.image_path)
        ):
            image_link = await self.s3_service.generate_link(user.image_path)

            image_link = HttpUrl(image_link)
            user.image_link = image_link
            new_img_link = f'{image_link.path}?{image_link.query}'

            bg_tasks.add_task(
                self.user_repo.change_one,
                user.id,
                {'image_link': new_img_link},
            )

        return user

    async def read_user_by_name(self, username: str) -> User:
        return await self.user_repo.find_one_by_custom_field(
            'username', username
        )

    async def read_user_with_role(self, id: int) -> User:
        return await self.user_repo.find_one(id, [self.user_repo.model.role])

    async def find_default_role(self) -> Role:
        default_role = await self.role_repo.find_one_by_custom_field(
            'name', 'client'
        )
        if not default_role:
            raise NoDefaultRoleError

        return default_role

    async def update_user(
        self,
        id: int,
        new_values: UserUpdate,
        avatar: UploadFile | None | str,
        bg_tasks: BackgroundTasks,
    ) -> UserReadWithRole:
        if new_values.password:
            hashed_pass = await self.password_service.a_get_pass_hash(
                new_values.password
            )
            new_values.hashed_password = hashed_pass

        if avatar:
            user = await self.read_entity(id)
            unique_filename = await self.s3_service.upload_file(
                S3Folders.AVATARS, avatar, user.image_path
            )

            new_values.image_path = unique_filename

        updated_user = await self.update_entity(id, new_values)
        return await self.add_img_link_to_user(
            UserRead.model_validate(updated_user), bg_tasks
        )

    async def delete_user(self, id: int) -> User:
        user = await self.user_repo.delete_one(id)
        await self.s3_service.remove_file(user.image_path)
        return user


AnnUserService = Annotated[UserService, Depends(UserService)]
