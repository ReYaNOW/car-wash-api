from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator
from pydantic.json_schema import SkipJsonSchema
from pydantic_core import Url
from pydantic_core.core_schema import ValidationInfo

from car_wash.config import config
from car_wash.storage.schemas import CustomBaseModel
from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class CarWashCreate(CustomBaseModel):
    name: str = Field(examples=['Spa Detailing'])
    location_id: int = Field(examples=[1])

    active: SkipJsonSchema[bool] = Field(default=False)
    image_path: SkipJsonSchema[str | None] = Field(default=None)


class CarWashRead(BaseModel):
    id: int
    name: str
    active: bool

    image_path: str | None = None
    image_link: HttpUrl | None = None

    location_id: int
    created_at: datetime

    class Config:
        from_attributes = True

    @field_validator('image_link', mode='before')
    @classmethod
    def convert_image_link(
        cls, v: str | HttpUrl, _: ValidationInfo
    ) -> HttpUrl | None:
        if not v:
            return None

        if isinstance(v, Url):
            return v

        if isinstance(v, str) and config.s3_server_url.host in v:
            return HttpUrl(v)
        return HttpUrl(f'{config.s3_server_url}{v.lstrip("/")}')


class CarWashList(GenericListRequest):
    order_by: Literal['id', 'name', 'location_id'] = 'id'
    active: bool | None = None


class CarWashUpdate(CustomBaseModel):
    name: str = Field(default=None, examples=['Spa Detailing'])
    location_id: int = Field(default=None, examples=[1])

    image_path: SkipJsonSchema[str | None] = Field(default=None)


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


class ShowHideResponse(BaseModel):
    status: str
