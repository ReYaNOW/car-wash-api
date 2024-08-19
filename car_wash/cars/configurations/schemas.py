from typing import Literal

from pydantic import BaseModel, Field

from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class ConfigurationCreate(BaseModel):
    generation_id: int = Field(examples=[1])
    body_type_id: int = Field(examples=[1])


class ConfigurationRead(BaseModel):
    id: int
    generation_id: int
    body_type_id: int

    class Config:
        from_attributes = True


class ConfigurationList(GenericListRequest):
    order_by: Literal['id', 'generation_id', 'body_type_id'] = 'id'
    generation_id: int | None = None
    body_type_id: int | None = None


class ConfigurationUpdate(BaseModel):
    generation_id: int = Field(default=None, examples=[1])
    body_type_id: int = Field(default=None, examples=[1])


class CreateResponse(BaseModel):
    configuration_id: int


class ReadResponse(ConfigurationRead):
    pass


class ListResponse(GenericListResponse):
    data: list[ConfigurationRead]


class UpdateResponse(ConfigurationRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
