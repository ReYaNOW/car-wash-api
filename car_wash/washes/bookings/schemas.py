from datetime import datetime, timedelta
from decimal import Decimal
from typing import Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    model_validator,
)
from pydantic.json_schema import SkipJsonSchema

from car_wash.cars.schemas import UserCarRead
from car_wash.utils.schemas import GenericListRequest, GenericListResponse
from car_wash.washes.boxes.schemas import BoxRead
from car_wash.washes.exceptions import (
    NotTwoHoursError,
    StartDatetimeGreaterError,
)
from car_wash.washes.locations.schemas import CarWashLocationRead


class BookingCreate(BaseModel):
    box_id: int = Field(examples=[1])
    user_car_id: int

    is_exception: bool = Field(default=False)

    start_datetime: datetime
    end_datetime: datetime

    price: SkipJsonSchema[Decimal | None] = Field(default=None)

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
    user_car_id: int
    user_car: UserCarRead

    box_id: int
    box: BoxRead = Field(exclude=True)

    price: Decimal | None

    is_accepted: bool
    is_completed: bool

    is_exception: bool

    start_datetime: datetime
    end_datetime: datetime

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def location(self) -> CarWashLocationRead:
        return self.box.car_wash.location


class BookingList(GenericListRequest):
    order_by: Literal['id', 'created_at', 'user_id', 'box_id'] = 'id'
    user_id: int | None = None
    box_id: int | None = None
    car_wash_id: int | None = None


class BookingUpdate(BookingCreate):
    box_id: int = Field(default=None, examples=[1])

    start_datetime: datetime = Field(default=None)
    end_datetime: datetime = Field(default=None)

    is_accepted: bool = Field(default=None)
    is_completed: bool = Field(default=None)
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
