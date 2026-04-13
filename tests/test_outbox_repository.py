import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

from src.domain.exceptions import NotFoundError
from src.infrastructure.db.models import OutboxStatus, TypeEvent
from src.infrastructure.repository.outbox import OutboxRepository


def test_get_outbox_maps_rows_to_entities():
    async def run():
        session = MagicMock()
        row = MagicMock()
        row.id = "o1"
        row.type_event = TypeEvent.buying
        row.payload = {"reference_id": "t1"}
        row.status = OutboxStatus.awaits
        row.retry = 1
        row.created_at = datetime.now(timezone.utc)

        result = MagicMock()
        scalars = MagicMock()
        scalars.all.return_value = [row]
        result.scalars.return_value = scalars
        session.execute = AsyncMock(return_value=result)

        repo = OutboxRepository(session)
        out = await repo.get_outbox()

        assert out is not None
        assert len(out) == 1
        assert out[0].id == "o1"
        assert out[0].payload["reference_id"] == "t1"

    asyncio.run(run())


def test_add_retry_increments_counter_and_commits():
    async def run():
        session = MagicMock()
        row = MagicMock()
        row.retry = 1
        result = MagicMock()
        result.scalar.return_value = row
        session.execute = AsyncMock(return_value=result)
        session.commit = AsyncMock()
        session.refresh = AsyncMock()

        repo = OutboxRepository(session)
        await repo.add_retry("o1")

        assert row.retry == 2
        session.commit.assert_awaited_once()
        session.refresh.assert_awaited_once_with(row)

    asyncio.run(run())


def test_change_outbox_status_sets_sent_and_commits():
    async def run():
        session = MagicMock()
        row = MagicMock()
        row.status = OutboxStatus.awaits
        result = MagicMock()
        result.scalar.return_value = row
        session.execute = AsyncMock(return_value=result)
        session.commit = AsyncMock()
        session.refresh = AsyncMock()

        repo = OutboxRepository(session)
        await repo.change_outbox_status("o1", "sent")

        assert row.status == OutboxStatus.sent
        session.commit.assert_awaited_once()
        session.refresh.assert_awaited_once_with(row)

    asyncio.run(run())


def test_change_outbox_status_raises_not_found_for_missing_row():
    async def run():
        session = MagicMock()
        result = MagicMock()
        result.scalar.return_value = None
        session.execute = AsyncMock(return_value=result)
        session.rollback = AsyncMock()

        repo = OutboxRepository(session)
        try:
            await repo.change_outbox_status("missing", "fail")
        except NotFoundError:
            pass
        else:
            raise AssertionError("NotFoundError was expected")

    asyncio.run(run())
