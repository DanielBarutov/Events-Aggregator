"""2fix retry for outbox

Revision ID: 2993ab971687
Revises: 76146a0230b6
Create Date: 2026-04-13 12:10:04.422237

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2993ab971687"
down_revision: Union[str, Sequence[str], None] = "76146a0230b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLE_NAME = "outbox"
COLUMN_NAME = "retry"


def _has_column(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = inspector.get_columns(table_name)
    return any(column["name"] == column_name for column in columns)


def upgrade() -> None:
    if not _has_column(TABLE_NAME, COLUMN_NAME):
        op.add_column(
            TABLE_NAME,
            sa.Column(
                COLUMN_NAME,
                sa.Integer(),
                nullable=True,
                server_default=sa.text("1"),
            ),
        )

    op.execute(
        sa.text(
            f"UPDATE {TABLE_NAME} SET {COLUMN_NAME} = 1 WHERE {COLUMN_NAME} IS NULL"
        )
    )

    op.alter_column(
        TABLE_NAME,
        COLUMN_NAME,
        existing_type=sa.Integer(),
        nullable=False,
        server_default=sa.text("1"),
    )


def downgrade() -> None:
    if _has_column(TABLE_NAME, COLUMN_NAME):
        op.drop_column(TABLE_NAME, COLUMN_NAME)
