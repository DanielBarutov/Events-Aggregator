import asyncio
import json
import httpx


class EventsPaginator:
    def __init__(self, base_url: str):
        self.client = EventsProviderClient(base_url=base_url)
        self.next_page_url = f"{self.client.base_url}/api/events/?changed_at=2000-01-01"

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.next_page_url is None:
            raise StopAsyncIteration

        data = await self.client.get_events(self.next_page_url)
        self.next_page_url = data.get("next").replace("http", "https")
        return data.get("results", [])


class EventsProviderClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.api_key = "nVtxYnXv3vO2P4hVNYlE6loBR-o6sJtFsVEtyGXi1As"

    async def get_events(self, url: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"x-api-key": self.api_key},
            )

            return response.json()


async def main():
    paginator = EventsPaginator(base_url="https://events-provider.dev-2.python-labs.ru")
    async for page in paginator:
        with open("events.json", "a") as f:
            json.dump(page, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
