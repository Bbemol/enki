"""test

Revision ID: fd55144271ea
Revises: 
Create Date: 2021-03-23 16:07:43.960573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd55144271ea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.get_context().autocommit_block():
        pass

def downgrade():
    op.execute("ALTER TYPE evenementtype RENAME TO evenementtype_old")
    op.execute("CREATE TYPE evenementtype AS ENUM('NATURAL', 'RASSEMBLEMENT')")
    op.execute((
        "ALTER TABLE transactions ALTER COLUMN status TYPE status USING "
        "status::text::status"
    ))
    op.execute("DROP TYPE evenementtype_old")
