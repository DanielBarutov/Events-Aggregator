from fastapi import APIRouter, Depends

from api.deps import manual_trigger_sync
from usecases.sync_events import SyncEventsUsecase


router = APIRouter(tags=["sync"])


@router.post("/sync/trigger")
async def trigger_sync(usecase: SyncEventsUsecase = Depends(manual_trigger_sync)):
    await usecase.execute()
    return {"status": "sync manual triggered successfully"}
