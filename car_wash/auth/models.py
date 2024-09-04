from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from car_wash.database import Base
from car_wash.users.models import User

metadata = Base.metadata


class RefreshToken(Base):
    __tablename__ = 'user__refresh_token'

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True, index=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey(User.id), unique=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
