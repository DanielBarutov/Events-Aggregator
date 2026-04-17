from fastapi import APIRouter, Response, Depends
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.infrastructure.observability.metrics import EVENTS_TOTAL
from src.infrastructure.repository.events import EventsRepository
from src.presentation.deps import get_events_repository

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
async def metrics(
    events_repository: EventsRepository = Depends(get_events_repository),
):
    count = await events_repository.count_events()
    EVENTS_TOTAL.set(count)
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
