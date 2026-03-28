"""
Тесты HTTP-клиента провайдера: httpx.AsyncClient подменяется,
реальный запрос в интернет не выполняется.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from infrastructure.clients.events_provider import EventsProviderClient


def test_get_by_url_replaces_http_with_https_in_next_and_previous():
    """Поля next/previous в JSON нормализуются с http на https."""

    async def run():
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "next": "http://api.example/next",
            "previous": "http://api.example/prev",
            "results": [],
        }
        mock_response.raise_for_status = MagicMock()

        inner_client = MagicMock()
        inner_client.get = AsyncMock(return_value=mock_response)
        inner_client.__aenter__ = AsyncMock(return_value=inner_client)
        inner_client.__aexit__ = AsyncMock(return_value=False)

        cm_factory = MagicMock(return_value=inner_client)

        with patch(
            "infrastructure.clients.events_provider.httpx.AsyncClient",
            cm_factory,
        ):
            provider = EventsProviderClient("https://api.example", "secret")
            data = await provider.get_by_url("/events/")

        assert data["next"] == "https://api.example/next"
        assert data["previous"] == "https://api.example/prev"
        inner_client.get.assert_awaited_once()
        # Заголовок API-ключа передаётся в запрос.
        _args, kwargs = inner_client.get.call_args
        assert kwargs["headers"] == {"x-api-key": "secret"}

    asyncio.run(run())


def test_get_by_url_passes_through_when_next_and_previous_are_falsy():
    """Если next/previous пустые или отсутствуют, код не падает."""

    async def run():
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "next": None,
            "previous": None,
            "results": [1],
        }
        mock_response.raise_for_status = MagicMock()

        inner_client = MagicMock()
        inner_client.get = AsyncMock(return_value=mock_response)
        inner_client.__aenter__ = AsyncMock(return_value=inner_client)
        inner_client.__aexit__ = AsyncMock(return_value=False)

        with patch(
            "infrastructure.clients.events_provider.httpx.AsyncClient",
            return_value=inner_client,
        ):
            provider = EventsProviderClient("https://x", "k")
            data = await provider.get_by_url("/")

        assert data["results"] == [1]
        assert data["next"] is None

    asyncio.run(run())
