import asyncio

from unittest.mock import AsyncMock, MagicMock

from utils.pagination import EventsPaginator


def test_paginator_yields_result_pages_and_stops_when_next_is_none():
    async def run():
        client = MagicMock()
        client.base_url = "https://provider.example"
        client.get_events = AsyncMock(
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
        assert client.get_events.await_count == 2
        assert paginator.next_page_url is None

    asyncio.run(run())


def test_paginator_first_request_uses_data_from_query():
    async def run():
        client = MagicMock()
        client.base_url = "https://x"
        client.get_events = AsyncMock(return_value={"next": None, "results": []})
        paginator = EventsPaginator(client, "2026-01-01")
        async for _ in paginator:
            pass
        client.get_events.assert_awaited_once_with(
            "https://x/api/events/?data_from=2026-01-01"
        )

    asyncio.run(run())
