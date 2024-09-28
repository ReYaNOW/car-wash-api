from typing import Self

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, model_validator

from car_wash.auth.exceptions import MissingCredentialsError
from car_wash.users.schemas import UserRead

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='jwt/token')


class AccessToken(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class Tokens(AccessToken):
    refresh_token: str


class TokenData(BaseModel):
    user_id: int | None = None


class UserCredentials(BaseModel):
    username: str | None = None
    password: str | None = None
    id: int | None = None

    @model_validator(mode='after')
    def validate(self) -> Self:
        if not self.id and not (self.username and self.password):
            raise MissingCredentialsError
        return self


class UserWithPass(UserRead):
    hashed_password: str = Field(default=None, exclude=True)

    class Config:
        from_attributes = True
