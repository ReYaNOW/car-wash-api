from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class UserCreate(BaseModel):
    username: str = Field(examples=['Username'])
    password: str = Field(examples=['password123'])
    first_name: str = Field(examples=['FirstName'])
    last_name: str = Field(examples=['LastName'])


class UserRead(BaseModel):
    id: int
    username: str
    password: str
    first_name: str
    last_name: str
    created_at: datetime


class UserList(GenericListRequest):
    order_by: Literal[
        'id', 'username', 'password', 'first_name', 'last_name', 'created_at'
    ] = 'id'


class UserUpdate(BaseModel):
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
