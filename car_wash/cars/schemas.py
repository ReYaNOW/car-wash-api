from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, computed_field, field_validator

from car_wash.cars.generations.schemas import GenerationRead
from car_wash.cars.utils import validate_year_range
from car_wash.utils.schemas import GenericListRequest


class CarCreate(BaseModel):
    name: str = Field(examples=['Audi A8 old'])
    body_type_id: int = Field(examples=[1])
    brand_id: int = Field(examples=[2])
    model: str = Field(examples=['A8'])

    year_range: str = Field(
        examples=['2003-2010', 'past-2010', '2003-present'], exclude=True
    )

    @computed_field
    @property
    def start_year(self) -> str:
        return self.year_range.split('-')[0]

    @computed_field
    @property
    def end_year(self) -> str:
        return self.year_range.split('-')[1]

    @field_validator('year_range')
    @classmethod
    def check_year_range(cls, v: str):
        validate_year_range(v)
        return v


class CarRead(BaseModel):
    id: int
    name: str
    body_type_id: int
    brand_id: int
    model: str
    generations: list[GenerationRead]
    start_year: int = Field(exclude=True)
    end_year: int = Field(exclude=True)
    created_at: datetime

    class Config:
        from_attributes = True

    @computed_field
    @property
    def year_range(self) -> str:
        year_start = self.start_year if self.start_year else 'past'
        year_end = self.end_year if self.end_year else 'present'
        if year_start == year_end:
            return 'all'
        return f'{year_start}-{year_end}'


class CarList(GenericListRequest):
    page: int
    limit: int = 10
    order_by: Literal[
        'id',
        'name',
        'body_type_id',
        'brand_id',
        'model',
        'generations',
        'year_start',
        'year_end',
        'created_at',
    ] = 'id'


class CarUpdate(CarCreate):
    name: str = Field(default=None, examples=['Audi A8 old'])
    body_type_id: int = Field(default=None, examples=[1])
    brand_id: int = Field(default=None, examples=[2])
    model: str = Field(default=None, examples=['A8'])

    year_range: str = Field(
        default=None,
        examples=['2003-2010', 'past-2010', '2003-present'],
        exclude=True,
    )


class CreateResponse(BaseModel):
    car_id: int


class ReadResponse(CarRead):
    pass


class UpdateResponse(CarRead):
    pass


class DeleteResponse(BaseModel):
    detail: str
