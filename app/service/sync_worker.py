import asyncio
from infrastructure.repository.sync import SyncMetadataRepository
from infrastructure.repository.events import EventsRepository
from infrastructure.clients.events_provider import EventsProviderClient
from infrastructure.db.session import AsyncSessionLocal
from usecases.sync_events import SyncEventsUsecase


async def run_sync_loop(usecase):
    while True:
        await asyncio.sleep(10)
        async with AsyncSessionLocal() as session:
            sync_repo = SyncMetadataRepository(session)
            events_repo = EventsRepository(session)
            usecase = SyncEventsUsecase(EventsProviderClient(), sync_repo, events_repo)
            await usecase.execute()
        await asyncio.sleep(86390)
