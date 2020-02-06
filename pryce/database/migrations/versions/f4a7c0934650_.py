"""empty message

Revision ID: f4a7c0934650
Revises: 576964f4fe91
Create Date: 2020-02-05 00:37:13.387357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4a7c0934650'
down_revision = '576964f4fe91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appuser', sa.Column('image', sa.String(), nullable=True))
    op.drop_constraint('appuser_avatar_fkey', 'appuser', type_='foreignkey')
    op.drop_column('appuser', 'avatar')
    op.add_column('badge', sa.Column('image', sa.String(), nullable=True))
    op.drop_column('badge', 'image_id')
    op.add_column('item', sa.Column('image', sa.String(), nullable=True))
    op.drop_constraint('item_image_id_fkey', 'item', type_='foreignkey')
    op.drop_column('item', 'image_id')
    op.add_column('store', sa.Column('image', sa.String(), nullable=True))
    op.drop_constraint('store_image_id_fkey', 'store', type_='foreignkey')
    op.drop_column('store', 'image_id')
    op.drop_table('image')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('store', sa.Column('image_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('store_image_id_fkey', 'store', 'image', ['image_id'], ['image_id'], onupdate='CASCADE', ondelete='RESTRICT')
    op.drop_column('store', 'image')
    op.add_column('item', sa.Column('image_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('item_image_id_fkey', 'item', 'image', ['image_id'], ['image_id'], onupdate='CASCADE', ondelete='RESTRICT')
    op.drop_column('item', 'image')
    op.add_column('badge', sa.Column('image_id', sa.BIGINT(), autoincrement=False, nullable=True))
    op.drop_column('badge', 'image')
    op.add_column('appuser', sa.Column('avatar', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('appuser_avatar_fkey', 'appuser', 'image', ['avatar'], ['image_id'], onupdate='CASCADE', ondelete='RESTRICT')
    op.drop_column('appuser', 'image')
    op.create_table('image',
    sa.Column('image_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('imgtype', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('width', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('height', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('uri', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('image_id', name='image_pkey'),
    sa.UniqueConstraint('uri', name='image_uri_key')
    )
    # ### end Alembic commands ###
