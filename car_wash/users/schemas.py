from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, computed_field, field_validator
from pydantic.json_schema import SkipJsonSchema
from pydantic_core import Url
from pydantic_core.core_schema import ValidationInfo

from car_wash.config import config
from car_wash.storage.schemas import CustomBaseModel
from car_wash.users.roles.schemas import RoleRead
from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class UserBase(CustomBaseModel):
    username: str = Field(examples=['Username'])
    password: str = Field(examples=['password123'], exclude=True)
    first_name: str = Field(examples=['FirstName'])
    last_name: str = Field(examples=['LastName'])

    image_path: SkipJsonSchema[str | None] = Field(default=None)
    hashed_password: SkipJsonSchema[str | None] = Field(default=None)

    @computed_field
    @property
    def confirmed(self) -> bool:
        return False

    @computed_field
    @property
    def active(self) -> bool:
        return True


class UserRegistration(UserBase):
    role_id: SkipJsonSchema[int | None] = Field(default=None)


class UserCreate(UserBase):
    role_id: int = Field(examples=[1])


class UserRead(BaseModel):
    id: int
    username: str

    first_name: str
    last_name: str

    image_path: str | None = None
    image_link: HttpUrl | None = None

    role_id: int
    confirmed: bool
    active: bool

    created_at: datetime

    class Config:
        from_attributes = True

    @field_validator('image_link', mode='before')
    @classmethod
    def convert_image_link(
        cls, v: str | HttpUrl, _: ValidationInfo
    ) -> HttpUrl | None:
        if not v:
            return None

        if isinstance(v, Url):
            return v

        if isinstance(v, str) and config.s3_server_url.host in v:
            return HttpUrl(v)
        return HttpUrl(f'{config.s3_server_url}{v.lstrip("/")}')


class UserReadWithRole(UserRead):
    role: RoleRead


class UserList(GenericListRequest):
    order_by: Literal[
        'id', 'username', 'password', 'first_name', 'last_name', 'created_at'
    ] = 'id'


class UserUpdate(CustomBaseModel):
    username: str | None = Field(default=None, examples=['Nameuser'])
    password: str | None = Field(
        default=None, examples=['123password'], exclude=True
    )
    first_name: str | None = Field(default=None, examples=['NameFirst'])
    last_name: str | None = Field(default=None, examples=['NameLast'])
    role_id: int | None = Field(default=None, examples=[1])

    image_path: SkipJsonSchema[str | None] = Field(default=None)
    hashed_password: SkipJsonSchema[str | None] = Field(default=None)


class CreateResponse(BaseModel):
    user_id: int


class ReadResponse(UserReadWithRole):
    pass


class ListResponse(GenericListResponse):
    data: list[UserRead]


class UpdateResponse(UserRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
