from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from car_wash.database import Base

metadata = Base.metadata


class CarWashLocation(Base):
    __tablename__ = 'car_wash__location'

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(64))
    address: Mapped[str] = mapped_column(String(64))

    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
