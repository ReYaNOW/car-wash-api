from datetime import datetime, timedelta
from decimal import Decimal
from typing import Literal, Self

from pydantic import BaseModel, Field, model_validator
from pydantic.json_schema import SkipJsonSchema

from car_wash.utils.schemas import GenericListRequest, GenericListResponse
from car_wash.washes.exceptions import (
    NotTwoHoursError,
    StartDatetimeGreaterError,
)


class BookingCreate(BaseModel):
    box_id: int = Field(examples=[1])
    user_car_id: int = Field(exclude=True)

    is_exception: bool = Field(default=False)

    start_datetime: datetime
    end_datetime: datetime

    price: SkipJsonSchema[Decimal | None] = Field(default=None)
    user_id: SkipJsonSchema[int | None] = Field(default=None)

    @model_validator(mode='after')
    def check_start_end_datetime(self) -> Self:
        if self.end_datetime < self.start_datetime:
            raise StartDatetimeGreaterError

        diff = self.end_datetime - self.start_datetime
        if not diff == timedelta(hours=2):
            raise NotTwoHoursError
        return self


class BookingRead(BaseModel):
    id: int
    user_id: int
    box_id: int

    price: Decimal | None
    is_exception: bool

    start_datetime: datetime
    end_datetime: datetime

    created_at: datetime

    class Config:
        from_attributes = True


class BookingList(GenericListRequest):
    order_by: Literal['id', 'created_at'] = 'id'
    user_id: int | None = None
    car_wash_id: int | None = None


class BookingUpdate(BookingCreate):
    box_id: int = Field(default=None, examples=[1])

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
