from sqlalchemy.dialects.postgresql import insert

from car_wash.auth.models import RefreshToken
from car_wash.database import async_session_maker
from car_wash.utils.repository import SQLAlchemyRepository


class RefreshTokenRepository(SQLAlchemyRepository):
    model = RefreshToken

    async def create_token_or_update(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            stmt = stmt.on_conflict_do_update(
                index_elements=['user_id'],
                set_=data,
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
