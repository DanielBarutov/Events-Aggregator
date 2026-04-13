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
            logger.info(f"Попытка отправить сообщение с: {url} : {header} : {payload}")

            response = await client.request(
                method="POST", url=url, headers=header, json=payload
            )
            logger.info(f"Запрос выполнен - {response}")

            response.raise_for_status()
            data = response.json()
            logger.info(f"Data: - {data}")
            print(data)
            return data
