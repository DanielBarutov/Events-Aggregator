import asyncio

from unittest.mock import AsyncMock, MagicMock
import pytest

from src.domain.exceptions import InputError, NotFoundError
from src.infrastructure.repository.events import EventsRepository


@pytest.fixture
def mock_session():
    session = MagicMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.merge = AsyncMock()
    session.delete = AsyncMock()
    return session


def test_create_events_adds_all_and_commits(mock_session):
    async def run():
        repo = EventsRepository(mock_session)
        place_entity = MagicMock()
        event_entity = MagicMock()

        repo.to_place_model = MagicMock(return_value="PLACE_MODEL")
        repo.to_event_model = MagicMock(return_value="EVENT_MODEL")

        await repo.sync(place_entity, event_entity)

        mock_session.merge.assert_any_await("PLACE_MODEL")
        mock_session.merge.assert_any_await("EVENT_MODEL")
        assert mock_session.merge.await_count == 2
        mock_session.commit.assert_awaited_once()

    asyncio.run(run())


def test_get_event_raises_not_found_for_missing_event(mock_session):
    async def run():
        result = MagicMock()
        result.scalar.return_value = None
        mock_session.execute = AsyncMock(return_value=result)

        repo = EventsRepository(mock_session)
        try:
            await repo.get_event("11111111-1111-1111-1111-111111111111")
        except NotFoundError as exc:
            assert exc.code == 404
        else:
            raise AssertionError("NotFoundError was expected")

    asyncio.run(run())


def test_get_event_raises_input_error_for_invalid_uuid(mock_session):
    async def run():
        repo = EventsRepository(mock_session)
        try:
            await repo.get_event("bad-id")
        except InputError as exc:
            assert exc.code == 400
        else:
            raise AssertionError("InputError was expected")

    asyncio.run(run())


def test_get_last_changed_at_returns_scalar_value(mock_session):
    async def run():
        result = MagicMock()
        result.scalar.return_value = "2026-03-31T10:00:00"
        mock_session.execute = AsyncMock(return_value=result)

        repo = EventsRepository(mock_session)
        out = await repo.get_last_changed_at()
        assert out == "2026-03-31T10:00:00"

    asyncio.run(run())
