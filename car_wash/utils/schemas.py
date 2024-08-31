from typing import TypeVar

from pydantic import BaseModel, computed_field

from car_wash.database import Base

T = TypeVar('T', bound=Base)


class GenericListRequest(BaseModel):
    page: int
    limit: int = 10
    order_by: str


class GenericListResponse(BaseModel):
    data: list
    total: int
    current: int

    @computed_field
    @property
    def previous(self) -> int | None:
        return self.current - 1 if self.current > 1 else None

    @computed_field
    @property
    def next(self) -> int | None:
        return self.current + 1 if self.current != self.total else None
