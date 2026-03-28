from fastapi import APIRouter

from infrastructure.clients.events_provider import EventsProviderClient
from usecases.sync_events import SyncEventsUsecase
import os

router = APIRouter(tags=["sync"])


@router.get("/trigger")
async def trigger_sync():
    usecase = SyncEventsUsecase(
        EventsProviderClient(
            base_url=os.getenv("EVENTS_PROVIDER_SERVER_URL_OUTSIDE"),
            api_key=os.getenv("EVENTS_PROVIDER_API_KEY"),
        )
    )
    await usecase.execute()
    return {"status": "sync triggered successfully"}
