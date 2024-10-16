from pydantic import BaseModel, Field, computed_field
from sqlalchemy import TableClause
from sqlalchemy.orm import Mapped


class AnyModel(TableClause):
    __tablename__ = 'any_model'

    id: Mapped[int]


class GenericListRequest(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1)


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
