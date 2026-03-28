from infrastructure.db.session import AsyncSessionLocal
from repository.events import EventsRepository
from utils.pagination import EventsPaginator
from infrastructure.clients.events_provider import EventsProviderClient
from infrastructure.mapper.events import EventsMapper


class SyncEventsUsecase:
    def __init__(self, client: EventsProviderClient):
        self.client = client
        self.repository = EventsRepository(AsyncSessionLocal())

    async def execute(self):
        paginator = EventsPaginator(self.client)
        async for events in paginator:
            await self.repository.upsert_places_and_events(
                EventsMapper(events).map_events(), EventsMapper(events).map_places()
            )

    async def get_last_sync_time(self):
        return await self.repository.get_last_changed_at()
