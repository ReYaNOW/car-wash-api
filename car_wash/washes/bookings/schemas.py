from datetime import datetime, timedelta
from decimal import Decimal
from enum import StrEnum, auto
from typing import Any, Literal, Self

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
from car_wash.washes.additions.schemas import CarWashAdditionRead
from car_wash.washes.boxes.schemas import BoxRead
from car_wash.washes.exceptions import (
    NotTwoHoursError,
    StartDatetimeGreaterError,
)
from car_wash.washes.locations.schemas import CarWashLocationRead
from car_wash.washes.models import Booking


class StateEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name: str, _: Any, __: Any, ___: Any) -> str:
        return name  # Возвращаем имя атрибута в верхнем регистре

    CREATED = auto()
    ACCEPTED = auto()
    STARTED = auto()
    COMPLETED = auto()
    EXCEPTION = auto()


class BookingCreate(BaseModel):
    box_id: int = Field(examples=[1])
    user_car_id: int = Field(examples=[1])

    state: StateEnum = Field(default=StateEnum.CREATED)
    notes: str | None = Field(examples=['Не открывать багажник!!!'])
    addition_ids: list[int] | None = Field(
        default=None, exclude=True, examples=[[]]
    )

    start_datetime: datetime
    end_datetime: datetime

    base_price: SkipJsonSchema[Decimal | None] = Field(default=None)
    total_price: SkipJsonSchema[Decimal | None] = Field(default=None)
    additions: SkipJsonSchema[Decimal | None] = Field(default=None)

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

    base_price: Decimal | None
    total_price: Decimal | None
    additions: list[CarWashAdditionRead]

    state: StateEnum
    notes: str | None

    start_datetime: datetime
    end_datetime: datetime

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def location(self) -> CarWashLocationRead:
        return self.box.car_wash.location

    @model_validator(mode='before')
    @classmethod
    def parse_additions(cls, data: Any) -> Any:
        if not isinstance(data, Booking):
            return data
        additions = data.additions

        if isinstance(additions, list) and additions:
            additions = [
                CarWashAdditionRead.model_validate_json(addition)
                for addition in additions
            ]
            data.additions = additions
        return data


class BookingList(GenericListRequest):
    order_by: Literal['id', 'created_at', 'user_id', 'box_id'] = 'id'
    user_id: int | None = None
    box_id: int | None = None
    car_wash_id: int | None = None


class BookingUpdate(BookingCreate):
    user_car_id: int | None = Field(default=None, examples=[1])
    box_id: int | None = Field(default=None, examples=[1])

    start_datetime: datetime | None = Field(default=None)
    end_datetime: datetime | None = Field(default=None)

    state: StateEnum | None = Field(default=None)
    notes: str | None = None


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
