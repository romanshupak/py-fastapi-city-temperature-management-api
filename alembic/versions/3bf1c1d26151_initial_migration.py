"""Initial migration

Revision ID: 3bf1c1d26151
Revises: 
Create Date: 2024-12-13 19:10:00.622733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bf1c1d26151'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('additional_info', sa.String(length=511), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_city_id'), 'city', ['id'], unique=False)
    op.create_table('Temperature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_time', sa.DateTime(), nullable=True),
    sa.Column('temperature', sa.Integer(), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Temperature_id'), 'Temperature', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Temperature_id'), table_name='Temperature')
    op.drop_table('Temperature')
    op.drop_index(op.f('ix_city_id'), table_name='city')
    op.drop_table('city')
    # ### end Alembic commands ###
