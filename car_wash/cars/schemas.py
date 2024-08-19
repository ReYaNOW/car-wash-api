from typing import Literal

from pydantic import BaseModel, Field, computed_field

from car_wash.utils.schemas import GenericListRequest


class UserCarCreate(BaseModel):
    name: str = Field(examples=['My lovely car'])
    user_id: int = Field(examples=[1])
    configuration_id: int = Field(examples=[1])

    @computed_field
    @property
    def is_verified(self) -> bool:
        return False


class UserCarRead(BaseModel):
    id: int
    name: str
    user_id: int
    configuration_id: int

    class Config:
        from_attributes = True


class UserCarList(GenericListRequest):
    order_by: Literal['id', 'name', 'user_id', 'configuration_id'] = 'id'


class UserCarUpdate(BaseModel):
    name: str = Field(default=None, examples=['My lovely car'])
    user_id: int = Field(default=None, examples=[1])
    configuration_id: int = Field(default=None, examples=[1])
    is_verified: bool = Field(default=None, examples=[False])


class CreateResponse(BaseModel):
    user_car_id: int


class ReadResponse(UserCarRead):
    pass


class UpdateResponse(UserCarRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
