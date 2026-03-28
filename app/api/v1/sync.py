from fastapi import APIRouter

router = APIRouter(tags=["sync"])


@router.get("/sync")
async def sync():
    return {"status": "ok"}
