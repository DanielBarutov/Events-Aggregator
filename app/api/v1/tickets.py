from fastapi import APIRouter

router = APIRouter(tags=["tickets"])


@router.get("/tickets")
async def get_tickets():
    return {"status": "ok"}
