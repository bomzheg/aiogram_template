"""add users

Revision ID: 0d453e730ac5
Revises: 
Create Date: 2023-07-19 10:39:55.338624

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0d453e730ac5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('tg_id', sa.BigInteger(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('is_bot', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__users')),
        sa.UniqueConstraint('tg_id', name=op.f('uq__users__tg_id'))
    )


def downgrade():
    op.drop_table('users')
