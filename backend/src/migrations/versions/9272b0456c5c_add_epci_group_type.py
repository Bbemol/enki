"""add epci group type

Revision ID: 9272b0456c5c
Revises: 0aabf94af7a7
Create Date: 2021-05-10 14:22:11.540456

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9272b0456c5c'
down_revision = '0aabf94af7a7'
branch_labels = None
depends_on = None


def upgrade():
    with op.get_context().autocommit_block():
        op.execute("""ALTER TYPE grouptype ADD VALUE IF NOT EXISTS 'EPCI';""")

def downgrade():
    pass