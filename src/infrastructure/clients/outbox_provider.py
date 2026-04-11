import logging
# from urllib.parse import urljoin

# import httpx


logger = logging.getLogger(__name__)


class OutboxProviderClient:
    def __init__(self, provider_url, provider_key):
        self.base_url = provider_url
        self.headers = {"x-api-key": provider_key}
        self.date = "data_from=2000-01-01"

    async def execute(self):
        pass
