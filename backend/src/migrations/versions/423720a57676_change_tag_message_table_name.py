"""change tag message table name

Revision ID: 423720a57676
Revises: 7f37af72c71e
Create Date: 2021-04-30 13:45:25.866669

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '423720a57676'
down_revision = '7f37af72c71e'
branch_labels = None
depends_on = None


def upgrade():
    pass
    #op.rename_table('tags_messages', 'messages_tags')


def downgrade():
    op.rename_table('messages_tags', 'tags_messages')