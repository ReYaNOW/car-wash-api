from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class BodyTypeCreate(BaseModel):
    name: str = Field(
        examples=['легковой автомобиль представительского класса']
    )


class BodyTypeRead(BaseModel):
    id: int
    name: str
    parent_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class BodyTypeList(GenericListRequest):
    order_by: Literal['id', 'name'] = 'id'
    name_like: str | None = Field(
        default=None, description='Search by substring'
    )


class BodyTypeUpdate(BaseModel):
    name: str = Field(
        default=None,
        examples=['легковой автомобиль представительского класса'],
    )


class CreateResponse(BaseModel):
    body_type_id: int


class ReadResponse(BodyTypeRead):
    pass


class ListResponse(GenericListResponse):
    data: list[BodyTypeRead]


class UpdateResponse(BodyTypeRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
