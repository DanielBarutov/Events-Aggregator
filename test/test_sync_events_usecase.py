"""
Тесты сценария SyncEventsUsecase: репозиторий и пагинатор подменяются моками,
чтобы проверить сценарий «страницы с клиента → сохранение в репозиторий».
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from usecases.sync_events import SyncEventsUsecase


def test_execute_iterates_paginator_and_persists_each_batch():
    """
    execute() обходит асинхронный пагинатор и для каждой порции results
    вызывает repository.create_events.
    """

    async def run():
        fake_client = MagicMock()

        class FakePaginator:
            """Имитация EventsPaginator: две «страницы» данных."""

            def __init__(self, _client):
                self._pages = [[MagicMock()], [MagicMock(), MagicMock()]]
                self._i = 0

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self._i >= len(self._pages):
                    raise StopAsyncIteration
                page = self._pages[self._i]
                self._i += 1
                return page

        mock_repo = MagicMock()
        mock_repo.create_events = AsyncMock()
        mock_repo.get_last_changed_at = AsyncMock(return_value="last-ts")

        with (
            patch("usecases.sync_events.EventsPaginator", FakePaginator),
            patch("usecases.sync_events.EventsRepository", return_value=mock_repo),
            patch("usecases.sync_events.get_session"),
        ):
            usecase = SyncEventsUsecase(fake_client)
            await usecase.execute()

        assert mock_repo.create_events.await_count == 2
        assert len(mock_repo.create_events.await_args_list[0].args[0]) == 1
        assert len(mock_repo.create_events.await_args_list[1].args[0]) == 2

    asyncio.run(run())


def test_get_last_sync_time_delegates_to_repository():
    """get_last_sync_time проксирует вызов в репозиторий."""

    async def run():
        mock_repo = MagicMock()
        mock_repo.get_last_changed_at = AsyncMock(return_value="2026-03-28T12:00:00")

        with (
            patch("usecases.sync_events.EventsRepository", return_value=mock_repo),
            patch("usecases.sync_events.get_session"),
        ):
            usecase = SyncEventsUsecase(MagicMock())
            assert await usecase.get_last_sync_time() == "2026-03-28T12:00:00"

        mock_repo.get_last_changed_at.assert_awaited_once()

    asyncio.run(run())
