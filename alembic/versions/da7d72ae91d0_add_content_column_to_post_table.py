"""add content column to post table

Revision ID: da7d72ae91d0
Revises: 3bfc3cc08d29
Create Date: 2023-06-24 13:00:33.524791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da7d72ae91d0'
down_revision = '3bfc3cc08d29'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
