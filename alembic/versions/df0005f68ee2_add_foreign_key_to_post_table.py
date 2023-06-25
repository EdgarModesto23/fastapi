"""add foreign key to post table

Revision ID: df0005f68ee2
Revises: deed46f9bd73
Create Date: 2023-06-24 13:13:56.494283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df0005f68ee2'
down_revision = 'deed46f9bd73'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users",
                          local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    


def downgrade():
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
