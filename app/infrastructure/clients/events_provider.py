import httpx

from shemas.event import EventListPydantic


class EventsProviderClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"x-api-key": api_key}

    async def get_events(self, url: str) -> EventListPydantic:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30) as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            return data

    # async def get_available_seats(self, event_id):
    # async with
