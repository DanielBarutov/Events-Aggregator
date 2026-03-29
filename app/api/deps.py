from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.session import get_session
from infrastructure.repository.events import EventsRepository
from usecases.get_events import (
    GetEventsUsecase,
    GetEventByIdUsecase,
    GetEventSeatsUsecase,
)


def get_events_repository(
    session: AsyncSession = Depends(get_session),
) -> EventsRepository:
    return EventsRepository(session)


def get_events_usecase(
    repository: EventsRepository = Depends(get_events_repository),
) -> GetEventsUsecase:
    return GetEventsUsecase(repository)


def get_event_by_id_usecase(
    repository: EventsRepository = Depends(get_events_repository),
) -> GetEventByIdUsecase:
    return GetEventByIdUsecase(repository)


def get_event_seats_usecase(
    repository: EventsRepository = Depends(get_events_repository),
) -> GetEventSeatsUsecase:
    return GetEventSeatsUsecase(repository)
