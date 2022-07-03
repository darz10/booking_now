"""Init migration

Revision ID: d907f9615904
Revises: 
Create Date: 2022-05-31 21:00:06.316324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd907f9615904'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('phone_number', sa.String(length=12), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('addresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('street', sa.String(length=150), nullable=False),
    sa.Column('building', sa.String(length=30), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('media_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_id', sa.String(length=150), nullable=False),
    sa.Column('source_fields', sa.JSON(), nullable=True),
    sa.Column('source_url', sa.String(length=200), nullable=True),
    sa.Column('uploaded', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('filename', sa.String(length=250), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.Column('url', sa.String(length=150), nullable=True),
    sa.Column('avatar', sa.String(length=250), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('type_place', sa.Enum('CAFE', 'BAR', 'RESTAURANT', name='placetype'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('place_branches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.Column('place_address_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['place_address_id'], ['addresses.id'], ),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('place_media_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.Column('file_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['file_id'], ['media_files.id'], ),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tables',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_favourite', sa.Boolean(), nullable=True),
    sa.Column('table_number', sa.Integer(), nullable=False),
    sa.Column('max_people', sa.Integer(), nullable=False),
    sa.Column('is_electricity', sa.Boolean(), nullable=True),
    sa.Column('floor', sa.Integer(), nullable=False),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.Column('place_branch_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['place_branch_id'], ['place_branches.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('table_number', 'place_branch_id', name='_table_place_branch_unique')
    )
    op.create_table('user_places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('place_branch_id', sa.Integer(), nullable=True),
    sa.Column('is_favourite', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['place_branch_id'], ['place_branches.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reservations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount_guests', sa.Integer(), nullable=True),
    sa.Column('date_reservation', sa.Date(), nullable=True),
    sa.Column('time_start', sa.Time(timezone=True), nullable=False),
    sa.Column('time_end', sa.Time(timezone=True), nullable=False),
    sa.Column('celebration', sa.Enum('BIRTHDAY', 'CORPORATE', 'WEDDING', 'FINAL_SCHOOL', name='celebrationtype'), nullable=True),
    sa.Column('note', sa.String(length=300), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('table_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['table_id'], ['tables.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservations')
    op.drop_table('user_places')
    op.drop_table('tables')
    op.drop_table('place_media_files')
    op.drop_table('place_branches')
    op.drop_table('places')
    op.drop_table('media_files')
    op.drop_table('addresses')
    op.drop_table('users')
    op.drop_table('cities')
    op.drop_table('roles')
    op.drop_table('countries')
    # ### end Alembic commands ###
