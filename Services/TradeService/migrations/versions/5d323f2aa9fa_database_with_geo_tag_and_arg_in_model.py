"""Database with Geo_tag and arg in model

Revision ID: 5d323f2aa9fa
Revises: 
Create Date: 2023-09-23 00:13:33.622033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d323f2aa9fa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('desciption', sa.String(), nullable=True, server_default=''),
        sa.Column('geo_tag', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'trades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('buyer_id', sa.Integer(), nullable=True),
        sa.Column('seller_id', sa.Integer(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('currency', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True, server_default=''),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('(now() at time zone \'utc\')')),
        sa.Column('geo_tag_id', sa.Integer(), nullable=True),
        sa.Column('hide', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['geo_tag_id'], ['tags.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('tags')
    op.drop_table('trades')