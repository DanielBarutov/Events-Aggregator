"""empty message

Revision ID: b7ce2cbbb033
Revises: 771abab20206
Create Date: 2026-03-28 10:33:26.624698

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7ce2cbbb033"
down_revision: Union[str, Sequence[str], None] = "771abab20206"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
