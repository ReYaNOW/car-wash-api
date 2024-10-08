from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
)

from car_wash.cars.utils import validate_year_range
from car_wash.utils.schemas import GenericListRequest, GenericListResponse


class GenerationCreate(BaseModel):
    name: str = Field(examples=['A5'])
    model_id: int = Field(examples=[1])

    year_range: str = Field(
        examples=['2003-2010', 'past-2010', '2003-present'], exclude=True
    )

    model_config = ConfigDict(protected_namespaces=())

    @computed_field
    @property
    def start_year(self) -> str | None:
        if self.year_range is None:
            return None
        return self.year_range.split('-')[0]

    @computed_field
    @property
    def end_year(self) -> str | None:
        if self.year_range is None:
            return None
        return self.year_range.split('-')[1]

    @field_validator('year_range')
    @classmethod
    def check_year_range(cls, v: str) -> str | None:
        if v is None:
            return None
        validate_year_range(v)
        return v


class GenerationRead(BaseModel):
    id: int
    name: str
    model_id: int
    start_year: int | str = Field(exclude=True)
    end_year: int | str = Field(exclude=True)

    model_config = ConfigDict(protected_namespaces=(), from_attributes=True)

    @computed_field
    @property
    def year_range(self) -> str:
        year_start = self.start_year if self.start_year else 'past'
        year_end = self.end_year if self.end_year else 'present'
        if year_start == year_end:
            return 'all'
        return f'{year_start}-{year_end}'


class GenerationList(GenericListRequest):
    order_by: Literal['id', 'name', 'model_id'] = 'id'
    name_like: str | None = Field(
        default=None, description='Search by substring'
    )
    model_id: int | None = None

    start_year: str | Literal['past'] | None = None
    end_year: str | Literal['present'] | None = None

    model_config = ConfigDict(protected_namespaces=())


class GenerationUpdate(GenerationCreate):
    name: str = Field(default=None, examples=['A5'])
    car_id: int = Field(default=None, examples=[1])

    year_range: str = Field(
        default=None,
        examples=['2003-2010', 'past-2010', '2003-present'],
        exclude=True,
    )


class CreateResponse(BaseModel):
    generation_id: int


class ReadResponse(GenerationRead):
    pass


class ListResponse(GenericListResponse):
    data: list[GenerationRead]


class UpdateResponse(GenerationRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
