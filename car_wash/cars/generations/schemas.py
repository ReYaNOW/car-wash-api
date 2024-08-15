from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from car_wash.utils.schemas import GenericListRequest


class GenerationCreate(BaseModel):
    name: str = Field(examples=['A5'])
    car_id: int = Field(examples=[1])


class GenerationRead(BaseModel):
    id: int
    name: str
    car_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class GenerationList(GenericListRequest):
    order_by: Literal['id', 'name', 'created_at'] = 'id'


class GenerationUpdate(BaseModel):
    name: str = Field(default=None, examples=['A5'])
    car_id: int = Field(default=None, examples=[1])


class CreateResponse(BaseModel):
    generation_id: int


class ReadResponse(GenerationRead):
    pass


class UpdateResponse(GenerationRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
