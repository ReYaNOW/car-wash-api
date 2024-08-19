from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from car_wash.utils.schemas import GenericListRequest


class ModelCreate(BaseModel):
    name: str = Field(examples=['M3'])
    brand_id: int = Field(examples=[1])


class ModelRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ModelList(GenericListRequest):
    order_by: Literal['id', 'name'] = 'id'
    name_like: str | None = Field(
        default=None, description='Search by substring'
    )
    brand_id: int | None = None


class ModelUpdate(BaseModel):
    name: str = Field(default=None, examples=['M3'])


class CreateResponse(BaseModel):
    model_id: int

    model_config = ConfigDict(protected_namespaces=())


class ReadResponse(ModelRead):
    pass


class UpdateResponse(ModelRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
