"""empty message

Revision ID: 516330b0185f
Revises: 82072d3419af
Create Date: 2025-01-08 17:13:52.545314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '516330b0185f'
down_revision: Union[str, None] = '82072d3419af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car_wash__addition',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('car_wash_id', sa.Integer(), nullable=False),
    sa.Column('additional_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['car_wash_id'], ['car_wash.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('car_wash', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('car_wash__booking', sa.Column('base_price', sa.Numeric(precision=10, scale=2), nullable=False))
    op.add_column('car_wash__booking', sa.Column('total_price', sa.Numeric(precision=10, scale=2), nullable=False))
    op.add_column('car_wash__booking', sa.Column('additions', sa.JSON(), nullable=False))
    op.add_column('car_wash__booking', sa.Column('state', sa.String(), nullable=False))
    op.add_column('car_wash__booking', sa.Column('notes', sa.Text(), nullable=True))
    op.drop_column('car_wash__booking', 'is_accepted')
    op.drop_column('car_wash__booking', 'is_completed')
    op.drop_column('car_wash__booking', 'is_exception')
    op.drop_column('car_wash__booking', 'price')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('car_wash__booking', sa.Column('price', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True))
    op.add_column('car_wash__booking', sa.Column('is_exception', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('car_wash__booking', sa.Column('is_completed', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('car_wash__booking', sa.Column('is_accepted', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('car_wash__booking', 'notes')
    op.drop_column('car_wash__booking', 'state')
    op.drop_column('car_wash__booking', 'additions')
    op.drop_column('car_wash__booking', 'total_price')
    op.drop_column('car_wash__booking', 'base_price')
    op.drop_column('car_wash', 'phone_number')
    op.drop_table('car_wash__addition')
    # ### end Alembic commands ###
