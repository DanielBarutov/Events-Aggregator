import asyncio

from fastapi import APIRouter, Depends, status

from src.presentation.deps import manual_trigger_sync
from src.application.usecases.sync_events import SyncEventsUsecase


router = APIRouter(tags=["sync"])


@router.post("/sync/trigger", status_code=status.HTTP_202_ACCEPTED)
async def trigger_sync(usecase: SyncEventsUsecase = Depends(manual_trigger_sync)):
    await asyncio.create_task(usecase.execute())
    return {"status": "sync manual triggered successfully"}
