import asyncio

from fastapi import APIRouter, status

from src.application.service.sync_manual import run_manual_sync


router = APIRouter(tags=["sync"])


@router.post("/sync/trigger", status_code=status.HTTP_202_ACCEPTED)
async def trigger_sync():
    asyncio.create_task(run_manual_sync())
    return {"status": "Sync manual triggered successfully"}
