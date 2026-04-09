import asyncio

from unittest.mock import AsyncMock, MagicMock, patch

from src.domain.exceptions import ExternalProviderError
from src.infrastructure.clients.events_provider import EventsProviderClient


def test_get_events():
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

        with patch(
            "src.infrastructure.clients.events_provider.httpx.AsyncClient",
            return_value=inner_client,
        ):
            provider = EventsProviderClient("http://api.example", "secret")
            data = await provider.get_events("http://api.example/api/events/")

        assert data["next"] == "https://api.example/next"
        assert data["previous"] == "https://api.example/prev"
        inner_client.get.assert_awaited_once()
        _, kwargs = inner_client.get.call_args
        assert kwargs["headers"] == {"x-api-key": "secret"}

    asyncio.run(run())


def test_get_available_seats_returns_seats_array():
    async def run():
        mock_response = MagicMock()
        mock_response.json.return_value = {"seats": ["A1", "A2"]}
        mock_response.raise_for_status = MagicMock()

        inner_client = MagicMock()
        inner_client.get = AsyncMock(return_value=mock_response)
        inner_client.__aenter__ = AsyncMock(return_value=inner_client)
        inner_client.__aexit__ = AsyncMock(return_value=False)

        with patch(
            "src.infrastructure.clients.events_provider.httpx.AsyncClient",
            return_value=inner_client,
        ):
            provider = EventsProviderClient("https://api.example", "secret")
            seats = await provider.get_available_seats("event-1")

        assert seats == ["A1", "A2"]

    asyncio.run(run())


def test_create_ticket_wraps_transport_errors():
    async def run():
        inner_client = MagicMock()
        inner_client.request = MagicMock(side_effect=RuntimeError("boom"))
        inner_client.__aenter__ = AsyncMock(return_value=inner_client)
        inner_client.__aexit__ = AsyncMock(return_value=False)

        with patch(
            "src.infrastructure.clients.events_provider.httpx.AsyncClient",
            return_value=inner_client,
        ):
            provider = EventsProviderClient("https://api.example", "secret")
            try:
                await provider.create_ticket(
                    "event-1", "Ivan", "Petrov", "test@test.com", "A1"
                )
            except ExternalProviderError as exc:
                assert exc.code == 502
                assert "создании тикета" in exc.message
            else:
                raise AssertionError("ExternalProviderError was expected")

    asyncio.run(run())
