from car_wash.auth.exceptions import refresh_token_is_used_exc
from car_wash.auth.schemas import Tokens, UserCredentials
from car_wash.auth.utils import PasswordService, TokenService, TokenType
from car_wash.users.schemas import UserRegistration
from car_wash.users.service import UserService


class AuthService:
    user_service = UserService
    token_service = TokenService
    password_service = PasswordService

    def __init__(self):
        self.user_service = self.user_service()
        self.token_service = self.token_service()
        self.password_service = self.password_service()

    async def register(self, new_user: UserRegistration) -> Tokens:
        user_id = await self.user_service.create_user(new_user)
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
            raise refresh_token_is_used_exc

        user = await self.user_service.authenticate_user(
            UserCredentials(id=user_id), auth_by='id'
        )
        access_token, refresh_token = self.token_service.create_tokens(
            sub=user.id
        )
        return Tokens(access_token=access_token, refresh_token=refresh_token)


async def get_auth_service() -> AuthService:
    return AuthService()
