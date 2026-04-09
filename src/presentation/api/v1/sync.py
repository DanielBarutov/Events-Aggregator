import asyncio
import logging

from fastapi import APIRouter, status

from src.infrastructure.db.session import AsyncSessionLocal
from src.infrastructure.clients.events_provider import EventsProviderClient
from src.infrastructure.repository.events import EventsRepository
from src.infrastructure.repository.sync import SyncMetadataRepository
from src.application.usecases.sync_events import SyncEventsUsecase


router = APIRouter(tags=["sync"])
logger = logging.getLogger(__name__)


async def run_manual_sync() -> None:
    async with AsyncSessionLocal() as session:
        sync_repo = SyncMetadataRepository(session)
        events_repo = EventsRepository(session)
        client = EventsProviderClient()
        usecase = SyncEventsUsecase(client, sync_repo, events_repo)
        try:
            await usecase.execute()
        except Exception:
            logger.exception("Manual sync background task failed")


@router.post("/sync/trigger", status_code=status.HTTP_202_ACCEPTED)
async def trigger_sync():
    asyncio.create_task(run_manual_sync())
    return {"status": "Sync manual triggered successfully"}
