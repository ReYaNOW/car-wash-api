from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from car_wash.database import Base

metadata = Base.metadata


class Role(Base):
    __tablename__ = 'user__role'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    users = relationship('User', back_populates='role')


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True)
    hashed_password: Mapped[str]

    first_name: Mapped[str]
    last_name: Mapped[str]

    image_path: Mapped[str] = mapped_column(nullable=True)
    image_link: Mapped[str] = mapped_column(nullable=True)

    confirmed: Mapped[bool] = mapped_column()
    active: Mapped[bool] = mapped_column()
    role_id: Mapped[int] = mapped_column(ForeignKey(Role.id))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    role = relationship('Role', back_populates='users')
    cars = relationship('UserCar', back_populates='user')
    bookings = relationship('Booking', back_populates='user')
