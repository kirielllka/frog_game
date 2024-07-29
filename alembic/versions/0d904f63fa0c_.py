"""empty message

Revision ID: 0d904f63fa0c
Revises: cd14690f69ed
Create Date: 2024-07-27 23:11:04.431847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d904f63fa0c'
down_revision: Union[str, None] = 'cd14690f69ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('frog', sa.Column('update_point', sa.Integer(), nullable=True))
    op.add_column('frog', sa.Column('max_lvl', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('frog', 'max_lvl')
    op.drop_column('frog', 'update_point')
    # ### end Alembic commands ###
