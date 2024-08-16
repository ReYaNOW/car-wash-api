from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from car_wash.utils.schemas import GenericListRequest


class CarWashLocationCreate(BaseModel):
    city: str = Field(examples=['Тараз'])
    address: str = Field(examples=['Айтиева'])


class CarWashLocationRead(BaseModel):
    id: int
    city: str
    address: str
    created_at: datetime

    class Config:
        from_attributes = True


class CarWashLocationList(GenericListRequest):
    order_by: Literal['id', 'city', 'address', 'created_at'] = 'id'


class CarWashLocationUpdate(BaseModel):
    city: str = Field(default=None, examples=['Тараз'])
    address: str = Field(default=None, examples=['Айтиева'])


class CreateResponse(BaseModel):
    location_id: int


class ReadResponse(CarWashLocationRead):
    pass


class UpdateResponse(CarWashLocationRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
