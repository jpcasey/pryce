"""remove not null constraint on item.description

Revision ID: 72e301ad1550
Revises: 6ff1853017d1
Create Date: 2020-02-07 21:26:43.169870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72e301ad1550'
down_revision = '6ff1853017d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('appuser', 'home',
               type_=sa.String(),
               nullable=True)
    op.alter_column('item', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('appuser', 'home',
                    type_=sa.INTEGER(),
                    nullable=True)
    op.alter_column('item', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###
