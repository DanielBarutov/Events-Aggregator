from fastapi import APIRouter

from shemas.event import EventPydantic
from usecases.get_events import GetEventsUsecase

router = APIRouter(tags=["events"])


@router.get("/events_all", response_model=list[EventPydantic])
async def get_all_events():
    usecase = GetEventsUsecase()
    return await usecase.execute()
