from car_wash.auth.models import RefreshToken
from car_wash.utils.repository import SQLAlchemyRepository


class RefreshTokenRepository(SQLAlchemyRepository):
    model = RefreshToken
