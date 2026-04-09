from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import src.setting
from src.infrastructure.repository.tickets import TicketsRepository
from src.infrastructure.repository.sync import SyncMetadataRepository
from src.infrastructure.repository.events import EventsRepository
from src.infrastructure.clients.events_provider import EventsProviderClient
from src.infrastructure.db.session import get_session
from src.application.usecases.create_ticket import TicketUsecase
from src.application.usecases.get_events import (
    GetEventsUsecase,
    GetEventByIdUsecase,
    GetEventSeatsUsecase,
)


def get_events_repository(
    session: AsyncSession = Depends(get_session),
) -> EventsRepository:
    return EventsRepository(session)


def sync_events_repository(
    session: AsyncSession = Depends(get_session),
) -> SyncMetadataRepository:
    return SyncMetadataRepository(session)


def get_tickets_repository(
    session: AsyncSession = Depends(get_session),
) -> TicketsRepository:
    return TicketsRepository(session)


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
    client = EventsProviderClient(
        src.setting.EVENTS_PROVIDER_SERVER, src.setting.EVENTS_PROVIDER_API_KEY
    )
    return GetEventSeatsUsecase(repository, client)


def get_tickets_usecase(
    event_repository: EventsRepository = Depends(get_events_repository),
    tickets_repository: TicketsRepository = Depends(get_tickets_repository),
) -> TicketUsecase:
    client = EventsProviderClient(
        src.setting.EVENTS_PROVIDER_SERVER, src.setting.EVENTS_PROVIDER_API_KEY
    )
    return TicketUsecase(client, event_repository, tickets_repository)
