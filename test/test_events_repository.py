"""
Тесты репозитория на уровне unit: AsyncSession из SQLAlchemy подменяется моком,
БД не поднимается.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from infrastructure.db.models import Event
from infrastructure.repository.events import EventsRepository


@pytest.fixture
def mock_session():
    """
    Сессия БД: у AsyncSession add_all синхронный, execute/commit — awaitable.
    Чистый AsyncMock помечал бы add_all как корутину и давал бы предупреждение.
    """
    session = MagicMock()
    session.add_all = MagicMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.merge = AsyncMock()
    session.delete = AsyncMock()
    return session


def test_create_events_adds_all_and_commits(mock_session):
    """create_events должен добавить все сущности и вызвать commit."""

    async def run():
        repo = EventsRepository(mock_session)
        e1, e2 = MagicMock(spec=Event), MagicMock(spec=Event)
        await repo.create_events([e1, e2])
        mock_session.add_all.assert_called_once_with([e1, e2])
        mock_session.commit.assert_awaited_once()

    asyncio.run(run())


def test_get_events_returns_list_from_session_execute(mock_session):
    """get_events мапит результат execute().scalars().all() в список."""

    async def run():
        row1, row2 = MagicMock(), MagicMock()
        scalars = MagicMock()
        scalars.all.return_value = [row1, row2]
        result = MagicMock()
        result.scalars.return_value = scalars
        mock_session.execute = AsyncMock(return_value=result)

        repo = EventsRepository(mock_session)
        out = await repo.get_events()

        assert out == [row1, row2]
        mock_session.execute.assert_awaited_once()

    asyncio.run(run())


def test_get_last_changed_at_returns_scalar(mock_session):
    """get_last_changed_at возвращает одно значение scalar() из запроса."""

    async def run():
        result = MagicMock()
        result.scalar.return_value = "ts-value"
        mock_session.execute = AsyncMock(return_value=result)

        repo = EventsRepository(mock_session)
        assert await repo.get_last_changed_at() == "ts-value"

    asyncio.run(run())


def test_update_events_merges_each_and_commits(mock_session):
    """update_events вызывает merge для каждой записи и commit в конце."""

    async def run():
        mock_session.merge = AsyncMock()
        repo = EventsRepository(mock_session)
        a, b = MagicMock(), MagicMock()
        await repo.update_events([a, b])
        assert mock_session.merge.await_args_list == [((a,),), ((b,),)]
        mock_session.commit.assert_awaited_once()

    asyncio.run(run())


def test_delete_events_deletes_each_and_commits(mock_session):
    """delete_events удаляет каждую сущность и делает commit."""

    async def run():
        mock_session.delete = AsyncMock()
        repo = EventsRepository(mock_session)
        x = MagicMock()
        await repo.delete_events([x])
        mock_session.delete.assert_awaited_once_with(x)
        mock_session.commit.assert_awaited_once()

    asyncio.run(run())
