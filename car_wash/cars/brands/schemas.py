from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class BrandCreate(BaseModel):
    name: str = Field(examples=['Audi'])


class BrandRead(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class BrandList(GenericListRequest):
    order_by: Literal['id', 'name', 'created_at'] = 'id'
    name_like: str | None = Field(
        default=None, description='Search by substring'
    )


class BrandUpdate(BaseModel):
    name: str = Field(default=None, examples=['Audi'])


class CreateResponse(BaseModel):
    brand_id: int


class ReadResponse(BrandRead):
    pass


class ListResponse(GenericListResponse):
    data: list[BrandRead]


class UpdateResponse(BrandRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
