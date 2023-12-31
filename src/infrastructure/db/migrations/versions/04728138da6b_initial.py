"""Initial

Revision ID: 04728138da6b
Revises: 
Create Date: 2023-12-16 19:16:58.935129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04728138da6b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'posts',
        sa.Column('title', sa.String(length=128), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('uuid', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('uuid', name=op.f('pk_posts')),
    )
    op.create_table(
        'users',
        sa.Column('username', sa.String(length=128), nullable=False),
        sa.Column('password', sa.String(length=60), nullable=False),
        sa.Column('disabled', sa.Boolean(), nullable=False),
        sa.Column('uuid', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('uuid', name=op.f('pk_users')),
        sa.UniqueConstraint('username', name=op.f('uq_users_username')),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('posts')
    # ### end Alembic commands ###
