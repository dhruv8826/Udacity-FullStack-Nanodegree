"""empty message

Revision ID: 8ce8fd28c000
Revises: 7951cd03de0b
Create Date: 2022-04-06 00:41:02.285777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ce8fd28c000'
down_revision = '7951cd03de0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('Artist', sa.Column('website_link', sa.String(length=300), nullable=True))
    op.add_column('Artist', sa.Column('looking_for_venues', sa.Boolean(), nullable=True))
    op.add_column('Artist', sa.Column('description', sa.String(), nullable=True))
    op.add_column('Artist', sa.Column('show_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Artist', 'Show', ['show_id'], ['id'])
    op.add_column('Venue', sa.Column('website_link', sa.String(length=300), nullable=True))
    op.add_column('Venue', sa.Column('looking_for_talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('description', sa.String(), nullable=True))
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('show_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Venue', 'Show', ['show_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'show_id')
    op.drop_column('Venue', 'genres')
    op.drop_column('Venue', 'description')
    op.drop_column('Venue', 'looking_for_talent')
    op.drop_column('Venue', 'website_link')
    op.drop_constraint(None, 'Artist', type_='foreignkey')
    op.drop_column('Artist', 'show_id')
    op.drop_column('Artist', 'description')
    op.drop_column('Artist', 'looking_for_venues')
    op.drop_column('Artist', 'website_link')
    op.drop_table('Show')
    # ### end Alembic commands ###