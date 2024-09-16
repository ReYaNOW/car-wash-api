from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class BoxCreate(BaseModel):
    name: str = Field(examples=['Первый'])
    car_wash_id: int = Field(examples=[1])
    user_id: int = Field(examples=[1])


class BoxRead(BaseModel):
    id: int
    name: str
    car_wash_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BoxList(GenericListRequest):
    order_by: Literal['id', 'car_wash_id'] = 'id'


class BoxUpdate(BaseModel):
    name: str = Field(default=None, examples=['Первый'])
    car_wash_id: int = Field(default=None, examples=[1])
    user_id: int = Field(default=None, examples=[1])


class CreateResponse(BaseModel):
    box_id: int


class ReadResponse(BoxRead):
    pass


class ListResponse(GenericListResponse):
    data: list[BoxRead]


class UpdateResponse(BoxRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
