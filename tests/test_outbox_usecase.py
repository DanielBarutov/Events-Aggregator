import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

from src.application.usecases.outbox import OutboxUsecase
from src.domain.models import OutboxEntity, OutboxStatus, OutboxTypeEvent


def test_outbox_usecase_returns_when_no_messages():
    async def run():
        repo = MagicMock()
        client = MagicMock()
        repo.get_outbox = AsyncMock(return_value=None)
        repo.add_retry = AsyncMock()
        repo.change_outbox_status = AsyncMock()
        client.execute = AsyncMock()

        usecase = OutboxUsecase(repo, client)
        await usecase.execute()

        repo.get_outbox.assert_awaited_once()
        repo.add_retry.assert_not_called()
        repo.change_outbox_status.assert_not_called()
        client.execute.assert_not_called()

    asyncio.run(run())


def test_outbox_usecase_marks_sent_on_successful_delivery():
    async def run():
        msg = OutboxEntity(
            id="o1",
            type_event=OutboxTypeEvent.buying,
            payload={"reference_id": "t1"},
            status=OutboxStatus.awaits,
            retry=1,
            created_at=datetime.now(timezone.utc),
        )
        repo = MagicMock()
        client = MagicMock()
        repo.get_outbox = AsyncMock(return_value=[msg])
        repo.add_retry = AsyncMock()
        repo.change_outbox_status = AsyncMock()
        client.execute = AsyncMock(return_value={"ok": True})

        usecase = OutboxUsecase(repo, client)
        await usecase.execute()

        repo.add_retry.assert_awaited_once_with("o1")
        client.execute.assert_awaited_once_with({"reference_id": "t1"})
        repo.change_outbox_status.assert_awaited_once_with("o1", "sent")

    asyncio.run(run())


def test_outbox_usecase_marks_fail_after_retry_limit():
    async def run():
        msg = OutboxEntity(
            id="o2",
            type_event=OutboxTypeEvent.buying,
            payload={"reference_id": "t2"},
            status=OutboxStatus.awaits,
            retry=4,
            created_at=datetime.now(timezone.utc),
        )
        repo = MagicMock()
        client = MagicMock()
        repo.get_outbox = AsyncMock(return_value=[msg])
        repo.add_retry = AsyncMock()
        repo.change_outbox_status = AsyncMock()
        client.execute = AsyncMock()

        usecase = OutboxUsecase(repo, client)
        await usecase.execute()

        repo.add_retry.assert_not_called()
        client.execute.assert_not_called()
        repo.change_outbox_status.assert_awaited_once_with("o2", "fail")

    asyncio.run(run())
