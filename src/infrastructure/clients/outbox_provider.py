import logging
from urllib.parse import urljoin

import httpx


logger = logging.getLogger(__name__)


class OutboxProviderClient:
    def __init__(self, provider_url, provider_key):
        self.base_url = provider_url
        self.provider_key = provider_key

    async def execute(self, payload):
        async with httpx.AsyncClient() as client:
            url = urljoin(self.base_url, "/api/notifications")
            header = {
                "Content-Type": "application/json",
                "x-api-key": self.provider_key,
            }
            response = await client.request(
                method="POST", url=url, headers=header, json=payload
            )
            logger.info(f"Запрос выполнен - {response}")
            data = response.json()
            if not response.is_success:
                logger.info(f"Был получен {response.status_code} игнорируем")
                return None
            return data
