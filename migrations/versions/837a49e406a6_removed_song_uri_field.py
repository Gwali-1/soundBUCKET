"""removed song uri field

Revision ID: 837a49e406a6
Revises: b5c8ef22135c
Create Date: 2023-05-04 14:54:22.557204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '837a49e406a6'
down_revision = 'b5c8ef22135c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('songs', 'song_uri')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('songs', sa.Column('song_uri', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
