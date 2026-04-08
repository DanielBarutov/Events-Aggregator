from urllib.parse import urljoin

from infrastructure.clients.events_provider import EventsProviderClient


class EventsPaginator:
    def __init__(self, client: EventsProviderClient, date: str | None = None):
        self.client = client
        self.next_page_url = urljoin(
            self.client.base_url, f"/api/events/?data_from={date}"
        )

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.next_page_url is None:
            raise StopAsyncIteration
        data = await self.client.get_events(self.next_page_url)
        self.next_page_url = data.get("next")
        return data.get("results", [])
