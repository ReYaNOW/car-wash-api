from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class CarWashAdditionCreate(BaseModel):
    car_wash_id: int = Field(examples=[1])
    name: str
    price: float = Field(examples=[500.0])


class CarWashAdditionRead(BaseModel):
    id: int
    name: str
    car_wash_id: int
    price: Decimal
    created_at: datetime

    class Config:
        from_attributes = True


class CarWashAdditionList(GenericListRequest):
    order_by: Literal['id', 'car_wash_id'] = 'id'
    car_wash_id: int | None = None


class CarWashAdditionUpdate(BaseModel):
    car_wash_id: int | None = Field(default=None, examples=[1])
    price: float | None = Field(default=None, examples=[500.0])


class CreateResponse(BaseModel):
    car_wash_addition_id: int


class CreateBulkResponse(BaseModel):
    car_wash_addition_ids: list[int]


class ReadResponse(CarWashAdditionRead):
    pass


class ListResponse(GenericListResponse):
    data: list[CarWashAdditionRead]


class UpdateResponse(CarWashAdditionRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
