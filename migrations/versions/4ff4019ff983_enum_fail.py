"""enum fail

Revision ID: 4ff4019ff983
Revises: 2993ab971687
Create Date: 2026-04-13 12:17:21.323422
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "4ff4019ff983"
down_revision: Union[str, Sequence[str], None] = "2993ab971687"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE outboxstatus ADD VALUE IF NOT EXISTS 'fail';")


def downgrade() -> None:
    pass
