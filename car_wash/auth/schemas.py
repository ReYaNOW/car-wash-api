from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, field_validator, model_validator

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
    def validate(self):
        if not self.id and not (self.username and self.password):
            raise ValueError('id or both username and password is required')
        return self


class UserForDB(UserRegistration):
    password: str = Field(exclude=True)
    hashed_password: str
    role_id: int

    @field_validator('hashed_password')
    def check_password_hashed(cls, v):
        if not pwd_context.identify(v):
            raise ValueError('Password must be hashed')
        return v


class UserInDB(UserRead):
    hashed_password: str = Field(default=None, exclude=True)

    class Config:
        from_attributes = True
