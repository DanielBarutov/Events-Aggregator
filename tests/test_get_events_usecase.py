from datetime import datetime, timezone

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from src.domain.exceptions import NotFoundError
from src.usecases.get_events import (
    GetEventByIdUsecase,
    GetEventSeatsUsecase,
    GetEventsUsecase,
)


def test_get_events_usecase_execute_sorts_desc_and_returns_page():
    async def run():
        repo = MagicMock()
        older = MagicMock(event_time=datetime(2026, 1, 1, tzinfo=timezone.utc))
        newer = MagicMock(event_time=datetime(2026, 2, 1, tzinfo=timezone.utc))
        repo.get_events_with_places = AsyncMock(return_value=[older, newer])

        with patch("usecases.get_events.EVENTS_PROVIDER_SERVER", "https://example.com"):
            result = await GetEventsUsecase(repo).execute(None, 1, 10)

        assert result["count"] == 2
        assert result["results"][0] is newer
        assert result["results"][1] is older

    asyncio.run(run())


def test_get_event_by_id_usecase_delegates_to_repository():
    async def run():
        repo = MagicMock()
        repo.get_event = AsyncMock(return_value={"id": "e1"})
        result = await GetEventByIdUsecase(repo).execute("e1")
        assert result == {"id": "e1"}
        repo.get_event.assert_awaited_once_with("e1")

    asyncio.run(run())


def test_get_event_seats_usecase_raises_not_found_for_unpublished():
    async def run():
        repo = MagicMock()
        client = MagicMock()
        repo.get_event = AsyncMock(return_value=MagicMock(status="draft"))

        usecase = GetEventSeatsUsecase(repo, client)
        try:
            await usecase.execute("event-1")
        except NotFoundError as exc:
            assert exc.code == 404
        else:
            raise AssertionError("NotFoundError was expected")

    asyncio.run(run())
