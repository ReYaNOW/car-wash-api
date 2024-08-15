from pydantic import BaseModel


class GenericListRequest(BaseModel):
    page: int
    limit: int = 10
    order_by: str
