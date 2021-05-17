"""test

Revision ID: 4f34195b9bda
Revises: 0c5a21b27a64
Create Date: 2021-04-20 13:27:01.290379

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4f34195b9bda'
down_revision = '0c5a21b27a64'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        DELETE FROM pg_enum
         WHERE enumtypid='evenementtype'::regtype
        AND enumlabel='INONDATION'
    """)
    with op.get_context().autocommit_block():
        pass
def downgrade():
    op.execute("ALTER TYPE evenementtype RENAME TO evenementtype_old")
    op.execute("CREATE TYPE evenementtype AS ENUM('INCENDIE', 'INONDATION','ATTENTAT')")
    op.execute((
        "ALTER TABLE transactions ALTER COLUMN status TYPE status USING "
        "status::text::status"
    ))
    op.execute("DROP TYPE evenementtype_old")