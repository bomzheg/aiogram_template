"""add table chats

Revision ID: e96680055f08
Revises: 4e570bc94610
Create Date: 2022-02-03 00:04:17.210338

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e96680055f08'
down_revision = '4e570bc94610'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'chats',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('tg_id', sa.BigInteger(), nullable=True),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('username', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tg_id'),
    )


def downgrade():
    op.drop_table('chats')
