import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from src.infrastructure.clients.outbox_provider import OutboxProviderClient


def test_outbox_provider_execute_sends_post_and_returns_json():
    async def run():
        payload = {"message": "ok", "reference_id": "t-1"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "accepted"}

        inner_client = MagicMock()
        inner_client.request = AsyncMock(return_value=mock_response)
        inner_client.__aenter__ = AsyncMock(return_value=inner_client)
        inner_client.__aexit__ = AsyncMock(return_value=False)

        with patch(
            "src.infrastructure.clients.outbox_provider.httpx.AsyncClient",
            return_value=inner_client,
        ):
            provider = OutboxProviderClient(
                "https://notify.example.com",
                "secret-key",
            )
            result = await provider.execute(payload)

        assert result == {"status": "accepted"}
        inner_client.request.assert_awaited_once()
        _, kwargs = inner_client.request.call_args
        assert kwargs["method"] == "POST"
        assert kwargs["url"] == "https://notify.example.com/api/notifications"
        assert kwargs["headers"]["x-api-key"] == "secret-key"
        assert kwargs["json"] == payload

    asyncio.run(run())
