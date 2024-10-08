"""empty message

Revision ID: 603a07342d3e
Revises: 1e4628efb2f4
Create Date: 2024-08-13 23:10:49.558545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '603a07342d3e'
down_revision: Union[str, None] = '1e4628efb2f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('frog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('lvl', sa.Integer(), nullable=True),
    sa.Column('strengh', sa.Integer(), nullable=True),
    sa.Column('agility', sa.Integer(), nullable=True),
    sa.Column('endurance', sa.Integer(), nullable=True),
    sa.Column('atack', sa.Integer(), nullable=True),
    sa.Column('update_point', sa.Integer(), nullable=True),
    sa.Column('max_lvl', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapons_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('attack', sa.Integer(), nullable=True),
    sa.Column('critic', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('frog_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['frog_id'], ['frog.id'], ),
    sa.ForeignKeyConstraint(['type'], ['weapons_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weapons')
    op.drop_table('weapons_category')
    op.drop_table('frog')
    # ### end Alembic commands ###
