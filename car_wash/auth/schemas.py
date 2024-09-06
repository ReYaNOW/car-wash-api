from typing import Self

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, field_validator, model_validator

from car_wash.auth.exceptions import (
    MissingCredentialsError,
    PasswordIsNotHashedError,
)
from car_wash.auth.utils import pwd_context
from car_wash.users.schemas import UserRead, UserRegistration

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


class UserForDB(UserRegistration):
    password: str = Field(exclude=True)
    hashed_password: str
    role_id: int

    @field_validator('hashed_password')
    @classmethod
    def check_hashed_password(cls, v: str) -> str:
        if not pwd_context.identify(v):
            raise PasswordIsNotHashedError
        return v


class UserInDB(UserRead):
    hashed_password: str = Field(default=None, exclude=True)

    class Config:
        from_attributes = True
