"""add chats

Revision ID: 812049d3a1da
Revises: 0d453e730ac5
Create Date: 2023-07-19 10:41:40.121286

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '812049d3a1da'
down_revision = '0d453e730ac5'
branch_labels = None
depends_on = None

chat_type = postgresql.ENUM('private', 'channel', 'group', 'supergroup', name='chattype', create_type=False)


def upgrade():
    chat_type.create(op.get_bind())
    op.create_table(
        'chats',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('tg_id', sa.BigInteger(), nullable=False),
        sa.Column('type', chat_type, nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__chats')),
        sa.UniqueConstraint('tg_id', name=op.f('uq__chats__tg_id'))
    )


def downgrade():
    op.drop_table('chats')
    chat_type.drop(op.get_bind())
