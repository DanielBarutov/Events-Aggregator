from fastapi import APIRouter, Depends
from api.deps import (
    get_events_usecase,
    get_event_by_id_usecase,
    get_event_seats_usecase,
)
from datetime import date
from shemas.event import EventPaginationPydantic, EventPydantic
from usecases.get_events import (
    GetEventByIdUsecase,
    GetEventSeatsUsecase,
    GetEventsUsecase,
)

router = APIRouter(tags=["events"])


@router.get("/events", response_model=EventPaginationPydantic)
async def get_events(
    data_from: date | None = None,
    page: int = 1,
    page_size: int = 20,
    usecase: GetEventsUsecase = Depends(get_events_usecase),
):
    return await usecase.execute(data_from, page, page_size)


@router.get("/events/{event_id}", response_model=EventPydantic)
async def get_event_by_id(
    event_id, usecase: GetEventByIdUsecase = Depends(get_event_by_id_usecase)
):
    return await usecase.execute(event_id)


@router.get("/events/{event_id}/seats")
async def get_event_seats(
    event_id, usecase: GetEventSeatsUsecase = Depends(get_event_seats_usecase)
):
    return await usecase.execute(event_id)
