from datetime import datetime

from pydantic import BaseModel, Field


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


class UserUpdate(BaseModel):
    username: str = Field(default=None, examples=['Nameuser'])
    password: str = Field(default=None, examples=['123password'])
    first_name: str = Field(default=None, examples=['NameFirst'])
    last_name: str = Field(default=None, examples=['NameLast'])


class CreateResponse(BaseModel):
    user_id: int


class ReadResponse(UserRead):
    pass


class UpdateResponse(UserRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
