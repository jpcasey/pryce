"""empty message

Revision ID: 54179a03702e
Revises: f4a7c0934650
Create Date: 2020-02-05 21:15:29.464105

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '54179a03702e'
down_revision = 'f4a7c0934650'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('appuser_home_fkey', 'appuser', type_='foreignkey')
    op.add_column('store', sa.Column('address', sa.String(), nullable=True))
    op.add_column('store', sa.Column('place_id', sa.String(), nullable=False))
    op.drop_constraint('store_location_id_fkey', 'store', type_='foreignkey')
    op.drop_column('store', 'location_id')
    op.drop_table('location')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('store', sa.Column('location_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('store_location_id_fkey', 'store', 'location', ['location_id'], ['location_id'], onupdate='CASCADE', ondelete='RESTRICT')
    op.drop_column('store', 'place_id')
    op.drop_column('store', 'address')
    op.create_foreign_key('appuser_home_fkey', 'appuser', 'location', ['home'], ['location_id'], onupdate='CASCADE', ondelete='RESTRICT')
    op.create_table('location',
    sa.Column('location_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('lat', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('long', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('location_id', name='location_pkey')
    )
    # ### end Alembic commands ###
