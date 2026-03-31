import httpx
import os
from shemas.event import EventListPydantic


class EventsProviderClient:
    def __init__(self):
        self.base_url = os.getenv("EVENTS_PROVIDER_SERVER_URL_OUTSIDE")
        self.headers = {"x-api-key": os.getenv("EVENTS_PROVIDER_API_KEY")}
        self.date = "data_from=2000-01-01"

    async def get_events(self, url: str, date: str | None = None) -> EventListPydantic:
        if date:
            self.date = f"data_from={date}"
        async with httpx.AsyncClient(base_url=self.base_url, timeout=60) as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data

    async def get_available_seats(self, event_id: str):
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            url = f"{self.base_url}/api/events/{event_id}/seats/"
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data["seats"]
