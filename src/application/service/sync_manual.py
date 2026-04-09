import logging

import src.setting
from src.infrastructure.repository.sync import SyncMetadataRepository
from src.infrastructure.repository.events import EventsRepository
from src.infrastructure.clients.events_provider import EventsProviderClient
from src.infrastructure.db.session import AsyncSessionLocal
from src.application.usecases.sync_events import SyncEventsUsecase

logger = logging.getLogger(__name__)


async def run_manual_sync() -> SyncEventsUsecase:
    async with AsyncSessionLocal() as session:
        sync_repo = SyncMetadataRepository(session)
        events_repo = EventsRepository(session)
        client = EventsProviderClient(
            src.setting.EVENTS_PROVIDER_SERVER, src.setting.EVENTS_PROVIDER_API_KEY
        )
        usecase = SyncEventsUsecase(client, sync_repo, events_repo)
        try:
            await usecase.execute()
        except Exception:
            logger.exception("Manual sync background task failed")
