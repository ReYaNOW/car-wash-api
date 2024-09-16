from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class CarWashCreate(BaseModel):
    name: str = Field(examples=['Spa Detailing'])
    location_id: int = Field(examples=[1])


class CarWashRead(BaseModel):
    id: int
    name: str
    location_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CarWashList(GenericListRequest):
    order_by: Literal['id', 'name', 'location_id'] = 'id'


class CarWashUpdate(CarWashCreate):
    name: str = Field(default=None, examples=['Spa Detailing'])
    location_id: int = Field(default=None, examples=[1])


class CreateResponse(BaseModel):
    car_wash_id: int


class ReadResponse(CarWashRead):
    pass


class ListResponse(GenericListResponse):
    data: list[CarWashRead]


class UpdateResponse(CarWashRead):
    pass


class DeleteResponse(BaseModel):
    detail: str


class AvailableTimesResponse(BaseModel):
    available_times: dict[int, list[tuple[datetime, datetime]]]
