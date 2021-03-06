"""removed 2 columns from post model

Revision ID: 9727d521db7f
Revises: b5da4b5527ec
Create Date: 2021-06-01 01:48:54.168510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9727d521db7f'
down_revision = 'b5da4b5527ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'image')
    op.drop_column('post', 'title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('post', sa.Column('image', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
