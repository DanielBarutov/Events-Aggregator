from infrastructure.clients.events_provider import EventsProviderClient


class EventsPaginator:
    def __init__(self, client: EventsProviderClient):
        self.client = client
        self.next_page_url = f"{self.client.base_url}/api/events/"

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.next_page_url is None:
            raise StopAsyncIteration

        data = await self.client.get_by_url(self.next_page_url)
        self.next_page_url = data.get("next")
        return data.get("results", [])
