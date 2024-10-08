from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class CarWashPriceCreate(BaseModel):
    car_wash_id: int = Field(examples=[1])
    body_type_id: int = Field(examples=[1])
    price: float = Field(examples=[500.0])


class CarWashPriceRead(BaseModel):
    id: int
    car_wash_id: int
    body_type_id: int
    price: float
    created_at: datetime

    class Config:
        from_attributes = True


class CarWashPriceList(GenericListRequest):
    order_by: Literal['id', 'car_wash_id', 'body_type_id'] = 'id'
    car_wash_id: int | None = None


class CarWashPriceUpdate(BaseModel):
    car_wash_id: int | None = Field(default=None, examples=[1])
    body_type_id: int | None = Field(default=None, examples=[1])
    price: float | None = Field(default=None, examples=[500.0])


class CreateResponse(BaseModel):
    car_wash_price_id: int


class CreateBulkResponse(BaseModel):
    car_wash_price_ids: list[int]


class ReadResponse(CarWashPriceRead):
    pass


class ListResponse(GenericListResponse):
    data: list[CarWashPriceRead]


class UpdateResponse(CarWashPriceRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
