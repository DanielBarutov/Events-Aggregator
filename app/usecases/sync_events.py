from utils.pagination import EventsPaginator
from infrastructure.clients.events_provider import EventsProviderClient
from infrastructure.mapper.events import EventsMapper


class SyncEventsUsecase:
    def __init__(self, client: EventsProviderClient, repository):
        self.client = client
        self.repository = repository

    async def execute(self):
        paginator = EventsPaginator(self.client)
        async for events in paginator:
            await self.repository.sync(
                EventsMapper(events).map_places(), EventsMapper(events).map_events()
            )

    async def get_last_sync_time(self):
        return await self.repository.get_last_changed_at()
