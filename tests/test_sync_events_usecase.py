import asyncio
from datetime import datetime, timezone

from unittest.mock import AsyncMock, MagicMock, patch

from src.domain.exceptions import BusinessLogicError
from src.domain.models import SyncStatusEntity
from src.usecases.sync_events import SyncEventsUsecase


def test_execute_runs_success_flow_and_updates_completed_status():
    async def run():
        sync_repo = MagicMock()
        sync_repo.get = AsyncMock(
            return_value=SyncStatusEntity(
                id="sync-1",
                last_sync_time=datetime(2026, 1, 1, 0, 0, 0),
                last_changed_at=datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                sync_status="completed",
            )
        )
        sync_repo.create = AsyncMock()
        sync_repo.update = AsyncMock()

        events_repo = MagicMock()
        events_repo.sync = AsyncMock()

        class FakeMapper:
            def __init__(self, event):
                self.event = event

            def map_places(self):
                return "PLACE_ENTITY"

            def map_events(self):
                return "EVENT_ENTITY"

        class FakePaginator:
            def __init__(self, _client, _date):
                self.pages = [
                    [
                        {"changed_at": "2026-02-01T12:00:00+00:00"},
                        {"changed_at": "2025-12-31T23:59:59+00:00"},
                    ]
                ]
                self.i = 0

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self.i >= len(self.pages):
                    raise StopAsyncIteration
                page = self.pages[self.i]
                self.i += 1
                return page

        with (
            patch("usecases.sync_events.EventsMapper", FakeMapper),
            patch("usecases.sync_events.EventsPaginator", FakePaginator),
        ):
            usecase = SyncEventsUsecase(MagicMock(), sync_repo, events_repo)
            await usecase.execute()

        sync_repo.create.assert_awaited_once()
        events_repo.sync.assert_awaited_once_with("PLACE_ENTITY", "EVENT_ENTITY")
        sync_repo.update.assert_awaited()
        status_arg = sync_repo.update.await_args.args[1]
        assert status_arg == "completed"

    asyncio.run(run())


def test_execute_marks_failed_and_raises_business_error_on_unexpected_exception():
    async def run():
        sync_repo = MagicMock()
        sync_repo.get = AsyncMock(
            return_value=SyncStatusEntity(
                id="sync-1",
                last_sync_time=datetime(2026, 1, 1, 0, 0, 0),
                last_changed_at=datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                sync_status="completed",
            )
        )
        sync_repo.create = AsyncMock()
        sync_repo.update = AsyncMock()

        events_repo = MagicMock()
        events_repo.sync = AsyncMock(side_effect=RuntimeError("db down"))

        class FakeMapper:
            def __init__(self, event):
                self.event = event

            def map_places(self):
                return "PLACE_ENTITY"

            def map_events(self):
                return "EVENT_ENTITY"

        class FakePaginator:
            def __init__(self, _client, _date):
                self.pages = [[{"changed_at": "2026-02-01T12:00:00+00:00"}]]
                self.i = 0

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self.i >= len(self.pages):
                    raise StopAsyncIteration
                page = self.pages[self.i]
                self.i += 1
                return page

        with (
            patch("usecases.sync_events.EventsMapper", FakeMapper),
            patch("usecases.sync_events.EventsPaginator", FakePaginator),
        ):
            usecase = SyncEventsUsecase(MagicMock(), sync_repo, events_repo)
            try:
                await usecase.execute()
            except BusinessLogicError:
                pass
            else:
                raise AssertionError("BusinessLogicError was expected")

        sync_repo.update.assert_awaited()
        status_arg = sync_repo.update.await_args.args[1]
        assert status_arg == "fail"

    asyncio.run(run())
