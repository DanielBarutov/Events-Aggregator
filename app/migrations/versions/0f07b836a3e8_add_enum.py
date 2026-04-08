"""add enum

Revision ID: 0f07b836a3e8
Revises: bbfbc18b9773
Create Date: 2026-04-08 19:07:47.923656

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "0f07b836a3e8"
down_revision: Union[str, Sequence[str], None] = "bbfbc18b9773"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


event_status_enum = postgresql.ENUM(
    "new",
    "published",
    "registration_closed",
    "finished",
    name="eventstatus",
)

sync_status_enum = postgresql.ENUM(
    "completed",
    "run",
    "fail",
    name="syncstatus",
)


def upgrade() -> None:
    bind = op.get_bind()

    # 1) create enum types first
    event_status_enum.create(bind, checkfirst=True)
    sync_status_enum.create(bind, checkfirst=True)

    # 2) alter columns to enum
    op.alter_column(
        "events",
        "status",
        existing_type=sa.VARCHAR(),
        type_=event_status_enum,
        existing_nullable=True,
        postgresql_using="status::eventstatus",
    )

    op.alter_column(
        "sync_status",
        "sync_status",
        existing_type=sa.VARCHAR(),
        type_=sync_status_enum,
        existing_nullable=False,
        postgresql_using="sync_status::syncstatus",
    )


def downgrade() -> None:
    bind = op.get_bind()

    # 1) back to varchar
    op.alter_column(
        "sync_status",
        "sync_status",
        existing_type=sync_status_enum,
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using="sync_status::text",
    )

    op.alter_column(
        "events",
        "status",
        existing_type=event_status_enum,
        type_=sa.VARCHAR(),
        existing_nullable=True,
        postgresql_using="status::text",
    )

    # 2) then drop enum types
    sync_status_enum.drop(bind, checkfirst=True)
    event_status_enum.drop(bind, checkfirst=True)
