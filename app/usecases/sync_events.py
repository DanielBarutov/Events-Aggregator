from datetime import datetime, timezone
import uuid as uuid_lib
from utils.pagination import EventsPaginator
from infrastructure.clients.events_provider import EventsProviderClient
from infrastructure.mapper.events import EventsMapper
from domain.models import SyncStatusEntity


class SyncEventsUsecase:
    def __init__(
        self, client: EventsProviderClient, sync_repository, events_repository
    ):
        self.client = client
        self.sync_repository = sync_repository
        self.events_repository = events_repository
        self.uuid = str(uuid_lib.uuid4())
        self.max_changed_at = datetime(2000, 1, 1, 0, 0, 0)

    async def execute(self):
        # try:
        last_sync: SyncStatusEntity = await self.get_sync()
        self.max_changed_at = last_sync.last_changed_at
        await self.start_sync()
        paginator = EventsPaginator(
            self.client, last_sync.last_changed_at.strftime("%Y-%m-%d")
        )
        async for events in paginator:
            for event in events:
                event_changed_at = datetime.fromisoformat(
                    event.get("changed_at")
                ).astimezone(timezone.utc)
                if event_changed_at > self.max_changed_at:
                    await self.events_repository.sync(
                        EventsMapper(event).map_places(),
                        EventsMapper(event).map_events(),
                    )
                    self.max_changed_at = event_changed_at

        # except Exception as e:
        # await self.fail()
        # raise e
        # finally:
        await self.end()

    async def start_sync(self):
        print("Начата сихронизация")
        return await self.sync_repository.create(self.uuid, "run")

    async def get_sync(self):
        return await self.sync_repository.get()

    async def end(self):
        print("Закончена сихронизация")
        return await self.sync_repository.update(
            self.uuid, "completed", self.max_changed_at
        )

    async def fail(self):
        return await self.sync_repository.update(self.uuid, "fail")
