"""Database with Geo_tag and arg in model

Revision ID: 5d323f2aa9fa
Revises: 
Create Date: 2023-09-23 00:13:33.622033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5d323f2aa9fa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('trades',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('buyer_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('seller_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('buyer_address', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('seller_address', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('currency', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('geo_tag_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('hide', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['geo_tag_id'], ['tags.id'], name='trades_geo_tag_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='trades_pkey')
    )
    op.create_table('tags',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('desciption', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('geo_tag', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='tags_pkey')
    )

def downgrade():
    op.drop_table('tags')
    op.drop_table('trades')