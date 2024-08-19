from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from car_wash.database import Base

metadata = Base.metadata


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[str]

    first_name: Mapped[str]
    last_name: Mapped[str]

    cars = relationship('UserCar', back_populates='user')

    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
