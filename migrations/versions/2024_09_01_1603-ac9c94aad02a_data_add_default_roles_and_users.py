"""[data] add default roles and users

Revision ID: ac9c94aad02a
Revises: 5e76a7f6e1c9
Create Date: 2024-09-01 16:03:46.713770

"""
import asyncio
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import select

from car_wash.auth.utils import PasswordService
from car_wash.config import config
from car_wash.database import async_session_maker
from car_wash.users.models import Role, User

# revision identifiers, used by Alembic.
revision: str = 'ac9c94aad02a'
down_revision: Union[str, None] = '5e76a7f6e1c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


token_service = PasswordService()
get_pass_hash = token_service.get_pass_hash


async def add_initial_data():
    async with async_session_maker() as session:
        admin_role = await session.execute(
            select(Role).filter_by(name='admin')
        )
        client_role = await session.execute(
            select(Role).filter_by(name='client')
        )

        if not admin_role.scalars().first():
            admin_role = Role(name='admin')
            session.add(admin_role)

        if not client_role.scalars().first():
            client_role = Role(name='client')
            session.add(client_role)

        await session.commit()

        admin_user = await session.execute(
            select(User).filter_by(username=config.admin_username)
        )
        client_user = await session.execute(
            select(User).filter_by(username='client')
        )

        if not admin_user.scalars().first():
            admin_role_result = await session.execute(
                select(Role).filter_by(name='admin')
            )
            admin_role = admin_role_result.scalars().first()

            hashed_pass = get_pass_hash(config.admin_password)
            admin_user = User(
                username=config.admin_username,
                hashed_password=hashed_pass,
                first_name='Admin',
                last_name='User',
                confirmed=True,
                active=True,
                role_id=admin_role.id,
            )
            session.add(admin_user)

        if not client_user.scalars().first():
            client_role_result = await session.execute(
                select(Role).filter_by(name='client')
            )
            client_role = client_role_result.scalars().first()

            hashed_pass = get_pass_hash('user_pass')
            client_user = User(
                username='client',
                hashed_password=hashed_pass,
                first_name='Client',
                last_name='User',
                confirmed=True,
                active=True,
                role_id=client_role.id,
            )
            session.add(client_user)

        await session.commit()


def upgrade():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(add_initial_data())


async def remove_initial_data():
    async with async_session_maker() as session:
        await session.execute(
            sa.delete(User).where(User.username.in_(['admin', 'client']))
        )
        await session.execute(
            sa.delete(Role).where(Role.name.in_(['admin', 'client']))
        )
        await session.commit()


def downgrade():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(remove_initial_data())
