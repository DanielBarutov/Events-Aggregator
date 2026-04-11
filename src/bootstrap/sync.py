from collections.abc import Awaitable, Callable

import src.setting
from src.application.usecases.sync_events import SyncEventsUsecase
from src.infrastructure.clients.events_provider import EventsProviderClient
from src.infrastructure.clients.mappers.client_mapper import EventsMapper
from src.infrastructure.repository.events import EventsRepository
from src.infrastructure.repository.sync import SyncMetadataRepository


def make_build_sync_usecase() -> Callable[[], Awaitable[SyncEventsUsecase]]:
    async def build_sync_usecase(session) -> SyncEventsUsecase:
        client = EventsProviderClient(
            src.setting.EVENTS_PROVIDER_SERVER,
            src.setting.EVENTS_PROVIDER_API_KEY,
        )
        mapper = EventsMapper()
        sync_repo = SyncMetadataRepository(session)
        events_repo = EventsRepository(session)
        return SyncEventsUsecase(client, mapper, sync_repo, events_repo)

    return build_sync_usecase
