"""create posts table

Revision ID: 3bfc3cc08d29
Revises: 
Create Date: 2023-06-24 12:51:57.754169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bfc3cc08d29'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title',sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
