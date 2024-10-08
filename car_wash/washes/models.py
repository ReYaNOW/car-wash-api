from datetime import datetime, time

from sqlalchemy import BigInteger, ForeignKey, Numeric, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from car_wash.cars.models import CarBodyType
from car_wash.database import Base
from car_wash.users.models import User
from car_wash.washes.locations.models import CarWashLocation

metadata = Base.metadata


class CarWash(Base):
    __tablename__ = 'car_wash'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    active: Mapped[bool]

    image_path: Mapped[str] = mapped_column(nullable=True)
    image_link: Mapped[str] = mapped_column(nullable=True)

    location_id: Mapped[int] = mapped_column(
        ForeignKey(CarWashLocation.id, ondelete='RESTRICT')
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    schedules: Mapped['Schedule'] = relationship(back_populates='car_wash')
    boxes: Mapped['Box'] = relationship(back_populates='car_wash')
    prices: Mapped['CarWashPrice'] = relationship(
        'CarWashPrice', back_populates='car_wash'
    )


class Schedule(Base):
    __tablename__ = 'car_wash__schedule'
    __table_args__ = (
        UniqueConstraint(
            'car_wash_id',
            'day_of_week',
            name='uix_car_wash_schedule___car_wash_id__day_of_week',
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    car_wash_id: Mapped[int] = mapped_column(
        ForeignKey(CarWash.id, ondelete='RESTRICT')
    )
    day_of_week: Mapped[int]  # День недели (Понедельник = 0, Воскресенье = 6)
    start_time: Mapped[time]
    end_time: Mapped[time]
    is_available: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relationships
    car_wash: Mapped['CarWash'] = relationship(
        'CarWash', back_populates='schedules'
    )


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

    # Relationships
    car_wash: Mapped['CarWash'] = relationship(
        'CarWash', back_populates='boxes'
    )
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
    price: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=True)

    start_datetime: Mapped[datetime]
    end_datetime: Mapped[datetime]

    is_exception: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relationships
    user: Mapped['User'] = relationship('User', back_populates='bookings')
    box: Mapped['Box'] = relationship('Box', back_populates='bookings')


class CarWashPrice(Base):
    __tablename__ = 'car_wash__price'
    __table_args__ = (
        UniqueConstraint(
            'car_wash_id',
            'body_type_id',
            name='uix_car_wash_price___car_wash_id__body_type_id',
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    car_wash_id: Mapped[int] = mapped_column(
        ForeignKey(CarWash.id, ondelete='CASCADE')
    )
    body_type_id: Mapped[int] = mapped_column(
        ForeignKey(CarBodyType.id, ondelete='CASCADE')
    )
    price: Mapped[Numeric] = mapped_column(Numeric(10, 2))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relationships
    car_wash: Mapped['CarWash'] = relationship(
        'CarWash', back_populates='prices'
    )
    body_type: Mapped['CarBodyType'] = relationship('CarBodyType')
