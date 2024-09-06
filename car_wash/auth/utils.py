from datetime import datetime, timedelta, timezone
from enum import Enum

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from starlette.concurrency import run_in_threadpool

from car_wash.auth.exceptions import (
    credentials_exc,
    expired_token_exc,
    invalid_token_type_exc,
)
from car_wash.auth.repository import RefreshTokenRepository
from car_wash.config import config
from car_wash.utils.repository import AnyModel

ALGORITHM = 'HS256'


class TokenType(Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'


class TokenService:
    secret_key = config.secret_key
    refresh_token_repo = RefreshTokenRepository

    def __init__(self):
        self.refresh_token_repo = self.refresh_token_repo()

    def create_tokens(self, sub: str | int) -> tuple[str, str]:
        access_token = self.create_jwt(sub=sub, token_type=TokenType.ACCESS)
        refresh_token = self.create_jwt(sub=sub, token_type=TokenType.ACCESS)
        return access_token, refresh_token

    def create_jwt(self, sub: str | int, token_type: TokenType) -> str:
        delta = (
            timedelta(days=config.refresh_token_expire_days)
            if token_type.value == TokenType.REFRESH
            else timedelta(minutes=config.access_token_expire_minutes)
        )
        expire = datetime.now(timezone.utc) + delta
        payload = {'sub': sub, 'exp': expire, 'type': token_type.value}
        encoded_jwt = jwt.encode(payload, self.secret_key, algorithm=ALGORITHM)
        return encoded_jwt

    def process_token(self, token: str, token_type: TokenType) -> int:
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[ALGORITHM]
            )
            if payload.get('type') != token_type.value:
                raise invalid_token_type_exc
            user_id: str = payload.get('sub')
            return int(user_id)
        except ExpiredSignatureError:
            raise expired_token_exc from None
        except InvalidTokenError:
            raise credentials_exc from None

    async def create_refresh_token_in_db(
        self, token: str, user_id: int
    ) -> int:
        return await self.refresh_token_repo.create_token_or_update(
            {'token': token, 'user_id': user_id}
        )

    async def read_token_by_user_id(self, user_id: int) -> AnyModel:
        return await self.refresh_token_repo.find_one_by_custom_field(
            'user_id', user_id
        )


async def get_token_service() -> TokenService:
    return TokenService()


pwd_context = CryptContext(
    schemes=['argon2'],
    argon2__memory_cost=4096,
    argon2__parallelism=2,
    deprecated='auto',
)


class PasswordService:
    @staticmethod
    def verify_pass(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def a_verify_pass(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return await run_in_threadpool(
            self.verify_pass, plain_password, hashed_password
        )

    @staticmethod
    def get_pass_hash(password: str) -> str:
        return pwd_context.hash(password)

    async def a_get_pass_hash(self, password: str) -> str:
        return await run_in_threadpool(self.get_pass_hash, password)
