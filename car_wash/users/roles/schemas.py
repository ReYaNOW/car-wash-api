from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class RoleCreate(BaseModel):
    name: Literal['client', 'admin']


class RoleRead(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class RoleList(GenericListRequest):
    order_by: Literal['id', 'name', 'created_at'] = 'id'
    name_like: str | None = Field(
        default=None, description='Search by substring'
    )


class RoleUpdate(BaseModel):
    name: str = Field(default=None, examples=['client'])


class CreateResponse(BaseModel):
    role_id: int


class ReadResponse(RoleRead):
    pass


class ListResponse(GenericListResponse):
    data: list[RoleRead]


class UpdateResponse(RoleRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
