from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class BookingCreate(BaseModel):
    car_wash_id: int = Field(examples=[1])

    start_datetime: datetime
    end_datetime: datetime

    is_exception: bool = Field(default=False)

    @model_validator(mode='after')
    def check_start_end_datetime(self):
        if self.end_datetime < self.start_datetime:
            raise ValueError(
                'start_datetime have to be lower then end_datetime'
            )
        return self


class BookingRead(BaseModel):
    id: int
    user_id: int
    car_wash_id: int

    start_datetime: datetime
    end_datetime: datetime

    is_exception: bool
    created_at: datetime

    class Config:
        from_attributes = True


class BookingList(GenericListRequest):
    order_by: Literal['id', 'created_at'] = 'id'


class BookingUpdate(BookingCreate):
    car_wash_id: int = Field(default=None, examples=[1])

    start_datetime: datetime = Field(default=None)
    end_datetime: datetime = Field(default=None)

    is_exception: bool = Field(default=None)


class CreateResponse(BaseModel):
    booking_id: int


class ReadResponse(BookingRead):
    pass


class ListResponse(GenericListResponse):
    data: list[BookingRead]


class UpdateResponse(BookingRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
