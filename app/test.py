import asyncio
import json
import os

from utils.pagination import EventsPaginator
from infrastructure.clients.events_provider import EventsProviderClient
from dotenv import load_dotenv

load_dotenv()


async def main():
    client = EventsProviderClient(
        base_url=os.getenv("EVENTS_PROVIDER_SERVER_URL_OUTSIDE"),
        api_key=os.getenv("EVENTS_PROVIDER_API_KEY"),
    )
    paginator = EventsPaginator(client)
    async for events in paginator:
        with open("events.json", "w") as f:
            json.dump(events, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    asyncio.run(main())
