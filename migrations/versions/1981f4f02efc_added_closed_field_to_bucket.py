"""added closed field to bucket

Revision ID: 1981f4f02efc
Revises: 2f417399f993
Create Date: 2023-04-21 13:51:56.560476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1981f4f02efc'
down_revision = '2f417399f993'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bucket', sa.Column('closed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bucket', 'closed')
    # ### end Alembic commands ###
