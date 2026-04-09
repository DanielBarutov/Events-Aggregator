import asyncio
from datetime import datetime, timezone

from unittest.mock import AsyncMock, MagicMock

from src.domain.exceptions import BusinessLogicError
from src.domain.models import SyncStatus, SyncStatusEntity
from src.application.usecases.sync_events import SyncEventsUsecase


def test_execute_runs_success_flow_and_updates_completed_status():
    async def run():
        sync_repo = MagicMock()
        sync_repo.get = AsyncMock(
            return_value=SyncStatusEntity(
                id="sync-1",
                last_sync_time=datetime(2026, 1, 1, 0, 0, 0),
                last_changed_at=datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                sync_status=SyncStatus.completed,
            )
        )
        sync_repo.create = AsyncMock()
        sync_repo.update = AsyncMock()

        events_repo = MagicMock()
        events_repo.sync = AsyncMock()

        mapper = MagicMock()
        mapper.map_places = MagicMock(return_value="PLACE_ENTITY")
        mapper.map_events = MagicMock(return_value="EVENT_ENTITY")

        class FakeClient:
            async def iter_events(self, _date):
                yield [
                    {"changed_at": "2026-02-01T12:00:00+00:00"},
                    {"changed_at": "2025-12-31T23:59:59+00:00"},
                ]

        usecase = SyncEventsUsecase(FakeClient(), mapper, sync_repo, events_repo)
        await usecase.execute()

        sync_repo.create.assert_awaited_once()
        events_repo.sync.assert_awaited_once_with("EVENT_ENTITY", "PLACE_ENTITY")
        sync_repo.update.assert_awaited()
        assert sync_repo.update.await_args_list[-1].args[1] == "completed"

    asyncio.run(run())


def test_execute_marks_failed_and_raises_business_error_on_unexpected_exception():
    async def run():
        sync_repo = MagicMock()
        sync_repo.get = AsyncMock(
            return_value=SyncStatusEntity(
                id="sync-1",
                last_sync_time=datetime(2026, 1, 1, 0, 0, 0),
                last_changed_at=datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                sync_status=SyncStatus.completed,
            )
        )
        sync_repo.create = AsyncMock()
        sync_repo.update = AsyncMock()

        events_repo = MagicMock()
        events_repo.sync = AsyncMock(side_effect=RuntimeError("db down"))

        mapper = MagicMock()
        mapper.map_places = MagicMock(return_value="PLACE_ENTITY")
        mapper.map_events = MagicMock(return_value="EVENT_ENTITY")

        class FakeClient:
            async def iter_events(self, _date):
                yield [{"changed_at": "2026-02-01T12:00:00+00:00"}]

        usecase = SyncEventsUsecase(FakeClient(), mapper, sync_repo, events_repo)
        try:
            await usecase.execute()
        except BusinessLogicError:
            pass
        else:
            raise AssertionError("BusinessLogicError was expected")

        sync_repo.update.assert_awaited()
        assert sync_repo.update.await_args_list[-1].args[1] == "fail"

    asyncio.run(run())
