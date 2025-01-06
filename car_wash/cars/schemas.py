from enum import Enum

from pydantic import BaseModel, Field, computed_field

from car_wash.users.schemas import UserReadWithRole
from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class UserCarCreate(BaseModel):
    name: str = Field(examples=['My lovely car'])
    configuration_id: int = Field(examples=[1])
    license_plate: str = Field(examples=['999AAA02'])

    @computed_field
    @property
    def is_verified(self) -> bool:
        return False


class UserCarRead(BaseModel):
    id: int
    name: str
    is_verified: bool
    license_plate: str
    configuration_id: int

    user: UserReadWithRole

    class Config:
        from_attributes = True


class OrderByEnum(str, Enum):
    id = 'id'
    name = 'name'
    user_id = 'user_id'
    configuration_id = 'configuration_id'


class UserCarList(GenericListRequest):
    order_by: OrderByEnum = OrderByEnum.id
    name_like: str | None = Field(
        default=None, description='Search by substring'
    )
    user_id: int | None = None
    configuration_id: int | None = None
    is_verified: bool | None = None


class UserCarUpdate(BaseModel):
    name: str = Field(default=None, examples=['My lovely car'])
    user_id: int = Field(default=None, examples=[1])
    configuration_id: int = Field(default=None, examples=[1])
    is_verified: bool = Field(default=None, examples=[False])


class CreateResponse(BaseModel):
    user_car_id: int


class ReadResponse(UserCarRead):
    pass


class ListResponse(GenericListResponse):
    data: list[UserCarRead]


class UpdateResponse(UserCarRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
