"""empty message

Revision ID: 023f95bfa315
Revises: b7ce2cbbb033
Create Date: 2026-03-28 10:35:32.174567

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "023f95bfa315"
down_revision: Union[str, Sequence[str], None] = "b7ce2cbbb033"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
