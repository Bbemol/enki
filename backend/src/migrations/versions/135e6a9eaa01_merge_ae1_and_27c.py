"""merge ae1 and 27c

Revision ID: 135e6a9eaa01
Revises: 423720a57676, a878d35f3dcb
Create Date: 2021-05-04 09:18:42.154417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '135e6a9eaa01'
down_revision = ('423720a57676', 'a878d35f3dcb')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
