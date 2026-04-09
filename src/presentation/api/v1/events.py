import datetime
import urllib

from fastapi import APIRouter, Depends

import src.setting
from src.presentation.deps import (
    get_events_usecase,
    get_event_by_id_usecase,
    get_event_seats_usecase,
)
from src.presentation.shemas.event import EventPaginationPydantic, EventPydantic
from src.application.usecases.get_events import (
    GetEventByIdUsecase,
    GetEventSeatsUsecase,
    GetEventsUsecase,
)

router = APIRouter(tags=["events"])


@router.get("/events", response_model=EventPaginationPydantic)
async def get_events(
    data_from: datetime.date | None = None,
    page: int = 1,
    page_size: int = 20,
    usecase: GetEventsUsecase = Depends(get_events_usecase),
):
    result = await usecase.execute(data_from)
    start = (page - 1) * page_size
    end = start + page_size
    count = len(result)
    next_page = page + 1
    prev_page = page - 1
    data_result = {
        "count": count,
        "next": urllib.parse.urljoin(
            src.setting.EVENTS_PROVIDER_SERVER, f"/api/events/?page={next_page}"
        )
        if next_page - 2 < (count // page_size)
        else None,
        "previous": urllib.parse.urljoin(
            src.setting.EVENTS_PROVIDER_SERVER, f"/api/events/?page={prev_page}"
        )
        if prev_page >= 1
        else None,
        "results": result[start:end],
    }
    return data_result


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
