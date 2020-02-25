"""Added NOT NULL constraint to item_id FK in price

Revision ID: c75b9013d2bb
Revises: 89822cb9c72b
Create Date: 2020-02-21 23:23:25.297911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c75b9013d2bb'
down_revision = '89822cb9c72b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('price', 'item_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('price', 'item_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###