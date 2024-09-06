from datetime import datetime, time
from typing import Literal, Self

from pydantic import BaseModel, Field, model_validator

from car_wash.utils.schemas import GenericListRequest, GenericListResponse
from car_wash.washes.schedules.exceptions import StartTimeGreaterError


class ScheduleCreate(BaseModel):
    car_wash_id: int = Field(examples=[1])
    day_of_week: int = Field(ge=0, le=6)

    start_time: time
    end_time: time

    is_available: bool

    @model_validator(mode='after')
    def check_start_end_time(self) -> Self:
        if self.end_time < self.start_time:
            raise StartTimeGreaterError
        return self


class ScheduleRead(BaseModel):
    id: int
    car_wash_id: int
    day_of_week: int

    start_time: time
    end_time: time

    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ScheduleList(GenericListRequest):
    order_by: Literal['id', 'created_at'] = 'id'


class ScheduleUpdate(ScheduleCreate):
    car_wash_id: int = Field(default=None, examples=[1])
    day_of_week: int = Field(default=None, ge=1, le=7)

    start_time: time = Field(default=None)
    end_time: time = Field(default=None)

    is_available: bool = Field(default=None)


class CreateResponse(BaseModel):
    schedule_id: int


class ReadResponse(ScheduleRead):
    pass


class ListResponse(GenericListResponse):
    data: list[ScheduleRead]


class UpdateResponse(ScheduleRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
