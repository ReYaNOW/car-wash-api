from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
)

from car_wash.cars.body_types.models import CarBodyType
from car_wash.cars.brands.models import CarBrand

Base = declarative_base()
metadata = Base.metadata


class CarGeneration(Base):
    __tablename__ = 'car_generation'

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey('car.id'))
    name: Mapped[str] = mapped_column(unique=True)

    car: Mapped['Car'] = relationship(back_populates='generations')

    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())


class Car(Base):
    __tablename__ = 'car'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    body_type_id: Mapped[int] = mapped_column(
        ForeignKey(CarBodyType.id, ondelete='RESTRICT')
    )
    brand_id: Mapped[int] = mapped_column(
        ForeignKey(CarBrand.id, ondelete='RESTRICT')
    )

    model: Mapped[str] = mapped_column(String(64))

    start_year: Mapped[int] = mapped_column(String(10))
    end_year: Mapped[int] = mapped_column(String(10))

    generations: Mapped[list['CarGeneration']] = relationship(
        back_populates='car'
    )

    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
