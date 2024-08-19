from datetime import datetime

from sqlalchemy import ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from car_wash.database import Base

metadata = Base.metadata


class CarBrand(Base):
    __tablename__ = 'car_brand'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    models: Mapped[list['CarModel']] = relationship(back_populates='brand')


class CarModel(Base):
    __tablename__ = 'car_model'
    __table_args__ = (
        UniqueConstraint(
            'name',
            'brand_id',
            name='uix_car_model__name_brand_id',
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    brand_id: Mapped[int] = mapped_column(
        ForeignKey(CarBrand.id, ondelete='RESTRICT')
    )
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    brand: Mapped['CarBrand'] = relationship(back_populates='models')
    generations: Mapped[list['CarGeneration']] = relationship(
        back_populates='model'
    )


class CarGeneration(Base):
    __tablename__ = 'car_generation'
    __table_args__ = (
        UniqueConstraint(
            'name',
            'model_id',
            name='uix_car_generation__name_model_id',
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    model_id: Mapped[int] = mapped_column(ForeignKey(CarModel.id))

    start_year: Mapped[int] = mapped_column(String(10))
    end_year: Mapped[int] = mapped_column(String(10))

    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    model: Mapped['CarModel'] = relationship(back_populates='generations')
    configurations: Mapped[list['CarConfiguration']] = relationship(
        back_populates='generation'
    )


class CarBodyType(Base):
    __tablename__ = 'car_body_type'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    configurations: Mapped[list['CarConfiguration']] = relationship(
        back_populates='body_type'
    )


class CarConfiguration(Base):
    __tablename__ = 'car_configuration'
    __table_args__ = (
        UniqueConstraint(
            'generation_id',
            'body_type_id',
            name='uix_car_configuration__generation_id_body_type_id',
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    generation_id: Mapped[int] = mapped_column(ForeignKey(CarGeneration.id))

    body_type_id: Mapped[str] = mapped_column(ForeignKey(CarBodyType.id))

    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    body_type: Mapped['CarBodyType'] = relationship(
        back_populates='configurations'
    )
    generation: Mapped['CarGeneration'] = relationship(
        back_populates='configurations'
    )
    user_cars: Mapped[list['UserCar']] = relationship(
        back_populates='configuration'
    )


class UserCar(Base):
    __tablename__ = 'user_car'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    user_id = mapped_column(ForeignKey('users.id', ondelete='RESTRICT'))
    configuration_id = mapped_column(
        ForeignKey(CarConfiguration.id, ondelete='RESTRICT')
    )
    is_verified: Mapped[bool]

    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    user = relationship('Users', back_populates='cars')
    configuration: Mapped['CarConfiguration'] = relationship(
        back_populates='user_cars'
    )
