"""New relations commit

Revision ID: f3339d1cb42e
Revises: d907f9615904
Create Date: 2022-07-21 20:25:10.011896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3339d1cb42e'
down_revision = 'd907f9615904'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('media_files', sa.Column('size', sa.Integer(), nullable=False))
    op.create_unique_constraint('unique_component_user', 'users', ['phone_number', 'email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_component_user', 'users', type_='unique')
    op.drop_column('media_files', 'size')
    # ### end Alembic commands ###
