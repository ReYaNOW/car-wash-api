from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()
metadata = Base.metadata


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[str]

    first_name: Mapped[str]
    last_name: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
