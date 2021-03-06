"""adeeded not null again

Revision ID: be4bfc49be90
Revises: f6f77752685c
Create Date: 2021-06-02 23:40:19.487730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be4bfc49be90'
down_revision = 'f6f77752685c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cart', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('order', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('cart', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
