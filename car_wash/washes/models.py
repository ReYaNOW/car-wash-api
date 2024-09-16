from datetime import datetime, time

from sqlalchemy import BigInteger, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from car_wash.database import Base
from car_wash.users.models import User
from car_wash.washes.locations.models import CarWashLocation

metadata = Base.metadata


class CarWash(Base):
    __tablename__ = 'car_wash'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location_id: Mapped[int] = mapped_column(
        ForeignKey(CarWashLocation.id, ondelete='RESTRICT')
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    schedules: Mapped['Schedule'] = relationship(back_populates='car_wash')
    boxes: Mapped['Box'] = relationship(back_populates='car_wash')


class Schedule(Base):
    __tablename__ = 'car_wash__schedule'

    id: Mapped[int] = mapped_column(primary_key=True)
    car_wash_id: Mapped[int] = mapped_column(
        ForeignKey(CarWash.id, ondelete='RESTRICT')
    )
    day_of_week: Mapped[int]  # День недели (Понедельник = 0, Воскресенье = 6)
    start_time: Mapped[time]
    end_time: Mapped[time]
    is_available: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    car_wash: Mapped['CarWash'] = relationship(back_populates='schedules')


class Box(Base):
    __tablename__ = 'car_wash__box'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    car_wash_id: Mapped[int] = mapped_column(
        ForeignKey(CarWash.id, ondelete='RESTRICT')
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete='RESTRICT')
    )

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    car_wash: Mapped['CarWash'] = relationship(back_populates='boxes')
    washer: Mapped['User'] = relationship('User')
    bookings: Mapped['Booking'] = relationship('Booking', back_populates='box')


class Booking(Base):
    __tablename__ = 'car_wash__booking'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete='RESTRICT')
    )
    box_id: Mapped[int] = mapped_column(
        ForeignKey(Box.id, ondelete='RESTRICT')
    )

    start_datetime: Mapped[datetime]
    end_datetime: Mapped[datetime]

    is_exception: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped['User'] = relationship(back_populates='bookings')
    box: Mapped['Box'] = relationship(back_populates='bookings')
