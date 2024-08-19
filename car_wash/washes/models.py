from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from car_wash.database import Base
from car_wash.washes.locations.models import CarWashLocation

metadata = Base.metadata


class CarWash(Base):
    __tablename__ = 'car_wash'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    boxes: Mapped[int]
    location_id: Mapped[int] = mapped_column(
        ForeignKey(CarWashLocation.id, ondelete='RESTRICT')
    )

    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
