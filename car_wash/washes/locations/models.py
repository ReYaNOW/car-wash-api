from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from car_wash.database import Base

if TYPE_CHECKING:
    from car_wash.washes.models import CarWash

metadata = Base.metadata


class CarWashLocation(Base):
    __tablename__ = 'car_wash__location'

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(64))
    address: Mapped[str] = mapped_column(String(64))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    car_washes: Mapped[list['CarWash']] = relationship(
        'CarWash', back_populates='location'
    )
