"""
Тесты пагинатора событий: клиент внешнего API подменяется моком,
чтобы не ходить в сеть и проверить только логику обхода страниц.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock

from utils.pagination import EventsPaginator


def test_paginator_yields_result_pages_and_stops_when_next_is_none():
    """
    EventsPaginator должен отдавать списки results по одному за раз
    и завершить асинхронную итерацию, когда в ответе нет следующей страницы.
    """

    async def run():
        # Мок клиента: get_by_url возвращает страницу с next, затем страницу без next.
        client = MagicMock()
        client.base_url = "https://provider.example"
        client.get_by_url = AsyncMock(
            side_effect=[
                {
                    "next": "https://provider.example/page2",
                    "results": [{"id": "a"}],
                },
                {"next": None, "results": [{"id": "b"}]},
            ]
        )

        paginator = EventsPaginator(client)
        pages = []
        async for batch in paginator:
            pages.append(batch)

        assert pages == [[{"id": "a"}], [{"id": "b"}]]
        assert client.get_by_url.await_count == 2
        # После второго ответа внутренний указатель next_page_url становится None.
        assert paginator.next_page_url is None

    asyncio.run(run())


def test_paginator_first_request_uses_events_list_url():
    """Первая загрузка идёт на {base_url}/api/events/ (как в реализации)."""

    async def run():
        client = MagicMock()
        client.base_url = "https://x"
        client.get_by_url = AsyncMock(return_value={"next": None, "results": []})
        paginator = EventsPaginator(client)
        async for _ in paginator:
            pass
        client.get_by_url.assert_awaited_once_with("https://x/api/events/")

    asyncio.run(run())
