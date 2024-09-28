from typing import Annotated

from fastapi import Depends, UploadFile

from car_wash.auth.exceptions import RefreshTokenIsUsedExc
from car_wash.auth.schemas import Tokens, UserCredentials
from car_wash.auth.utils import (
    AnnPassService,
    AnnTokenService,
    PasswordService,
    TokenService,
    TokenType,
)
from car_wash.users.schemas import UserRegistration
from car_wash.users.service import AnnUserService, UserService


class AuthService:
    user_service = UserService
    token_service = TokenService
    password_service = PasswordService

    def __init__(
        self,
        user_service: AnnUserService,
        token_service: AnnTokenService,
        pass_service: AnnPassService,
    ):
        self.user_service = user_service
        self.token_service = token_service
        self.password_service = pass_service

    async def register(
        self, new_user: UserRegistration, img: UploadFile | None
    ) -> Tokens:
        user_id = await self.user_service.create_user(new_user, img)
        access_token, refresh_token = self.token_service.create_tokens(
            sub=user_id
        )
        await self.token_service.create_refresh_token_in_db(
            refresh_token, user_id
        )
        return Tokens(access_token=access_token, refresh_token=refresh_token)

    async def login(self, username: str, password: str) -> Tokens:
        user = await self.user_service.authenticate_user(
            UserCredentials(username=username, password=password),
            auth_by='username_and_pass',
        )
        access_token, refresh_token = self.token_service.create_tokens(
            sub=user.id
        )
        await self.token_service.create_refresh_token_in_db(
            refresh_token, user.id
        )
        return Tokens(access_token=access_token, refresh_token=refresh_token)

    async def refresh_tokens(self, token: str) -> Tokens:
        user_id = self.token_service.process_token(
            token, token_type=TokenType.REFRESH
        )
        token_in_db = await self.token_service.read_token_by_user_id(
            user_id=user_id
        )

        if token_in_db.token != token:
            raise RefreshTokenIsUsedExc

        user = await self.user_service.authenticate_user(
            UserCredentials(id=user_id), auth_by='id'
        )
        access_token, refresh_token = self.token_service.create_tokens(
            sub=user.id
        )
        return Tokens(access_token=access_token, refresh_token=refresh_token)


AnnAuthService = Annotated[AuthService, Depends(AuthService)]
