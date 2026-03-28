from fastapi import APIRouter
from datetime import date
from shemas.event import EventPaginationPydantic, EventPydantic
from usecases.get_events import GetEventsUsecase, GetEventById

router = APIRouter(tags=["events"])


@router.get("/events", response_model=EventPaginationPydantic)
async def get_events(
    data_from: date | None = None,
    page: int = 1,
    page_size: int = 20,
):
    usecase = GetEventsUsecase()
    return await usecase.execute(data_from, page, page_size)


@router.get("/events/{event_id}", response_model=EventPydantic)
async def get_event_by_id(event_id):
    usecase = GetEventById()
    return await usecase.execute(event_id)
