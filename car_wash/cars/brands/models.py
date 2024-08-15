from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()
metadata = Base.metadata


class CarBrand(Base):
    __tablename__ = 'car_brand'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
