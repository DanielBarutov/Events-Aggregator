from fastapi import APIRouter

router = APIRouter(tags=["events"])


@router.get("/events")
async def get_events():
    return {"status": "ok"}
