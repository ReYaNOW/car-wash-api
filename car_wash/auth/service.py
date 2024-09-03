from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic import ValidationError

from car_wash.auth.exceptions import (
    credentials_exc,
    expired_token_exc,
    invalid_token_type_exc,
    refresh_token_is_used_exc,
)
from car_wash.auth.repository import RefreshTokenRepository
from car_wash.auth.schemas import (
    TokenData,
    Tokens,
    UserCredentials,
    UserForDB,
    UserInDB,
)
from car_wash.auth.utils import (
    get_pass_hash_in_threadpool,
    verify_password_in_threadpool,
)
from car_wash.config import config
from car_wash.users.models import User
from car_wash.users.repository import UserRepository
from car_wash.users.roles.repository import RoleRepository
from car_wash.users.schemas import UserRegistration
from car_wash.utils.schemas import T

ALGORITHM = 'HS256'


class AuthService:
    user_repository = UserRepository
    role_repository = RoleRepository
    refresh_token_repository = RefreshTokenRepository

    def __init__(self):
        self.user_repo = self.user_repository()
        self.role_repo = self.role_repository()
        self.refresh_token_repo = self.refresh_token_repository()

    async def register(self, new_user: UserRegistration) -> Tokens:
        default_role = await self.role_repo.find_one_by_custom_field(
            'name', 'client'
        )
        if not default_role:
            raise ValueError('Cant find default role with name "client"')

        user_dict = new_user.model_dump()
        hashed_pass = await get_pass_hash_in_threadpool(new_user.password)

        user_for_db = UserForDB(
            **user_dict, hashed_password=hashed_pass, role_id=default_role.id
        )
        user_id = await self.user_repo.add_one(user_for_db.model_dump())
        access_token, refresh_token = self.create_tokens(sub=user_id)

        await self.create_refresh_token_in_db(refresh_token, user_id)
        return Tokens(access_token=access_token, refresh_token=refresh_token)

    async def login(self, username: str, password: str) -> Tokens:
        user = await self.authenticate_user(
            UserCredentials(username=username, password=password),
            auth_by='username_and_pass',
        )
        access_token, refresh_token = self.create_tokens(sub=user.id)

        await self.create_refresh_token_in_db(refresh_token, user.id)
        return Tokens(access_token=access_token, refresh_token=refresh_token)

    async def refresh_tokens(self, token: str):
        token_data = self.process_token(token, token_type='refresh')
        token_in_db = await self.read_token_by_user_id(
            user_id=token_data.user_id
        )

        if token_in_db.token != token:
            raise refresh_token_is_used_exc

        user = await self.authenticate_user(
            UserCredentials(id=token_data.user_id), auth_by='id'
        )
        access_token, refresh_token = self.create_tokens(sub=user.id)
        return Tokens(access_token=access_token, refresh_token=refresh_token)

    def create_tokens(self, sub: Any):
        access_token = self.create_jwt(sub=sub, token_type='access')
        refresh_token = self.create_jwt(sub=sub, token_type='refresh')
        return access_token, refresh_token

    def create_jwt(self, sub, token_type: Literal['access', 'refresh']) -> str:
        if token_type == 'refresh':
            delta = timedelta(days=config.refresh_token_expire_days)
        else:
            delta = timedelta(minutes=config.access_token_expire_minutes)

        expire = datetime.now(timezone.utc) + delta

        payload = {'sub': sub, 'exp': expire, 'type': token_type}
        encoded_jwt = jwt.encode(
            payload, config.secret_key, algorithm=ALGORITHM
        )
        return encoded_jwt

    def process_token(
        self, token: str, token_type: Literal['access', 'refresh']
    ):
        try:
            payload = self.decode_token(token)
            if payload.get('type') != token_type:
                raise invalid_token_type_exc

            user_id: str = payload.get('sub')
            return TokenData(user_id=user_id)
        except ExpiredSignatureError:
            raise expired_token_exc from None
        except (InvalidTokenError, ValidationError):
            raise credentials_exc from None

    def decode_token(self, token: str | bytes) -> dict:
        return jwt.decode(token, config.secret_key, algorithms=[ALGORITHM])

    async def authenticate_user(
        self,
        user_credentials: UserCredentials,
        auth_by: Literal['id', 'username_and_pass'],
    ) -> UserInDB:
        if auth_by == 'id':
            user = await self.read_user_with_role(user_credentials.id)
            return UserInDB.model_validate(user)

        else:
            user = await self.read_user_by_name(user_credentials.username)

        if not user:
            raise credentials_exc

        hashed_password = user.hashed_password
        if not await verify_password_in_threadpool(
            user_credentials.password, hashed_password
        ):
            raise credentials_exc

        return UserInDB.model_validate(user)

    async def read_user_with_role(self, id: int) -> User:
        return await self.user_repo.find_one(id, [self.user_repo.model.role])

    async def read_token_by_user_id(self, user_id: int) -> T:
        return await self.refresh_token_repo.find_one_by_custom_field(
            'user_id', user_id
        )

    async def create_refresh_token_in_db(self, token: str, user_id: int):
        return await self.refresh_token_repo.add_one(
            {'token': token, 'user_id': user_id}
        )

    async def read_user_by_name(self, username) -> User:
        return await self.user_repo.find_one_by_custom_field(
            'username', username
        )
