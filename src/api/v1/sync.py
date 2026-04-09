import asyncio

from fastapi import APIRouter, Depends, status

from src.api.deps import manual_trigger_sync
from src.usecases.sync_events import SyncEventsUsecase


router = APIRouter(tags=["sync"])


@router.post("/sync/trigger", status_code=status.HTTP_202_ACCEPTED)
async def trigger_sync(usecase: SyncEventsUsecase = Depends(manual_trigger_sync)):
    asyncio.create_task(usecase.execute())
    return {"status": "sync manual triggered successfully"}
