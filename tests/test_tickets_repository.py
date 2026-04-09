import asyncio

from unittest.mock import AsyncMock, MagicMock

from src.domain.exceptions import NotFoundError
from src.infrastructure.repository.tickets import TicketsRepository


def _session_mock():
    session = MagicMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.delete = AsyncMock()
    session.add = MagicMock()
    return session


def test_get_ticket_returns_not_found_when_absent():
    async def run():
        session = _session_mock()
        result = MagicMock()
        result.scalar.return_value = None
        session.execute = AsyncMock(return_value=result)
        repo = TicketsRepository(session)

        try:
            await repo.get_ticket("missing")
        except NotFoundError as exc:
            assert exc.code == 404
        else:
            raise AssertionError("NotFoundError was expected")

    asyncio.run(run())


def test_delete_ticket_deletes_loaded_entity_and_commits():
    async def run():
        session = _session_mock()
        ticket = MagicMock()
        result = MagicMock()
        result.scalar.return_value = ticket
        session.execute = AsyncMock(return_value=result)
        repo = TicketsRepository(session)

        await repo.delete_ticket("t-1")

        session.delete.assert_awaited_once_with(ticket)
        session.commit.assert_awaited_once()

    asyncio.run(run())
