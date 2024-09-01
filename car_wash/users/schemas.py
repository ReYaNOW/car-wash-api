from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, computed_field

from car_wash.users.roles.schemas import RoleRead
from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class UserRegistration(BaseModel):
    username: str = Field(examples=['Username'])
    password: str = Field(examples=['password123'])
    first_name: str = Field(examples=['FirstName'])
    last_name: str = Field(examples=['LastName'])

    @computed_field
    @property
    def confirmed(self) -> bool:
        return False

    @computed_field
    @property
    def active(self) -> bool:
        return True


class UserCreate(UserRegistration):
    role_id: int


class UserRead(BaseModel):
    id: int
    username: str

    first_name: str
    last_name: str

    role_id: int
    confirmed: bool
    active: bool

    created_at: datetime

    class Config:
        from_attributes = True


class UserReadWithRole(UserRead):
    role: RoleRead


class UserList(GenericListRequest):
    order_by: Literal[
        'id', 'username', 'password', 'first_name', 'last_name', 'created_at'
    ] = 'id'


class UserUpdate(UserCreate):
    username: str = Field(default=None, examples=['Nameuser'])
    password: str = Field(default=None, examples=['123password'])
    first_name: str = Field(default=None, examples=['NameFirst'])
    last_name: str = Field(default=None, examples=['NameLast'])


class CreateResponse(BaseModel):
    user_id: int


class ReadResponse(UserRead):
    pass


class ListResponse(GenericListResponse):
    data: list[UserRead]


class UpdateResponse(UserRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
