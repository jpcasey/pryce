"""Initial migration

Revision ID: 7bc6eb79e09b
Revises: 
Create Date: 2020-01-30 16:28:46.130563

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import FetchedValue 

# revision identifiers, used by Alembic.
revision = '7bc6eb79e09b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('access',
    sa.Column('access_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('access_id')
    )
    op.create_table('badge',
    sa.Column('badge_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('image_id', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('badge_id')
    )
    op.create_table('chain',
    sa.Column('chain_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('chain_id')
    )
    op.create_table('image',
    sa.Column('image_id', sa.Integer(), nullable=False),
    sa.Column('fspath', sa.String(), nullable=True),
    sa.Column('imgtype', sa.String(), nullable=True),
    sa.Column('width', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('image_id'),
    sa.UniqueConstraint('fspath')
    )
    op.create_table('location',
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('long', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('location_id')
    )
    op.create_table('appuser',
    sa.Column('appuser_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('home', sa.Integer(), nullable=True),
    sa.Column('karma', sa.Integer(), nullable=True),
    sa.Column('avatar', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['avatar'], ['image.image_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['home'], ['location.location_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('appuser_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('item',
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('brand', sa.String(), nullable=True),
    sa.Column('weight', sa.Numeric(), nullable=False),
    sa.Column('weight_unit', sa.String(), server_default=FetchedValue(), nullable=True),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['image.image_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('item_id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('store',
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('chain_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chain_id'], ['chain.chain_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['image_id'], ['image.image_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['location_id'], ['location.location_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('store_id')
    )
    op.create_table('badge_appuser',
    sa.Column('badge_id', sa.Integer(), nullable=False),
    sa.Column('appuser_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['appuser_id'], ['appuser.appuser_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['badge_id'], ['badge.badge_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('badge_id', 'appuser_id')
    )
    op.create_table('comment',
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('appuser_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Numeric(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.CheckConstraint('(content IS NOT NULL) OR (rating IS NOT NULL)'),
    sa.ForeignKeyConstraint(['appuser_id'], ['appuser.appuser_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('object_id', 'type')
    )
    op.create_table('list',
    sa.Column('list_id', sa.Integer(), nullable=False),
    sa.Column('owner', sa.Integer(), nullable=True),
    sa.Column('access_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['access_id'], ['access.access_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['owner'], ['appuser.appuser_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('list_id')
    )
    op.create_table('price',
    sa.Column('price_id', sa.Integer(), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('appuser_id', sa.Integer(), nullable=True),
    sa.Column('price', postgresql.MONEY(), nullable=True),
    sa.Column('reported', sa.DateTime(timezone=True), nullable=True),
    sa.Column('store_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['appuser_id'], ['appuser.appuser_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['item_id'], ['item.item_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['store_id'], ['store.store_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('price_id')
    )
    op.create_table('list_item',
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('list_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), server_default=FetchedValue(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['item.item_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['list_id'], ['list.list_id'], ),
    sa.ForeignKeyConstraint(['list_id'], ['list.list_id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('item_id', 'list_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('list_item')
    op.drop_table('price')
    op.drop_table('list')
    op.drop_table('comment')
    op.drop_table('badge_appuser')
    op.drop_table('store')
    op.drop_table('item')
    op.drop_table('appuser')
    op.drop_table('location')
    op.drop_table('image')
    op.drop_table('chain')
    op.drop_table('badge')
    op.drop_table('access')
    # ### end Alembic commands ###