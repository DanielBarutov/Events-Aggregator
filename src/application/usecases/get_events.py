import datetime
import logging

from src.domain.models import EventEntity
from src.domain.exceptions import AppError, BusinessLogicError, NotFoundError
from src.application.ports.event_provider_port import EventProviderPort
from src.application.ports.repo.get_events_repo import GetEventsRepositoryPort


logger = logging.getLogger(__name__)


class GetEventsUsecase:
    def __init__(self, repository: GetEventsRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, data_from: datetime.date) -> list[EventEntity]:
        try:
            result = await self.repository.get_events_with_places(data_from)
            sorted_result = sorted(result, key=lambda x: x.event_time, reverse=True)
            return sorted_result
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении событий",
                extra={"data_from": data_from},
            )
            raise BusinessLogicError(
                "Неизвестная ошибка при получении событий", details={"reason": str(e)}
            )


class GetEventByIdUsecase:
    def __init__(self, repository: GetEventsRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, event_id) -> EventEntity:
        return await self.repository.get_event(event_id)


class GetEventSeatsUsecase:
    def __init__(
        self, repository: GetEventsRepositoryPort, client: EventProviderPort
    ) -> None:
        self.repository = repository
        self.client = client

    async def execute(self, event_id) -> dict:
        try:
            event: EventEntity = await self.repository.get_event(event_id)
            if not event:
                raise NotFoundError(
                    "Событие не найдено", details={"event_id": event_id}
                )
            if event.status != "published":
                raise NotFoundError(
                    "Событие не имеет статус published", details={"event_id": event_id}
                )
            available_seats = await self.client.get_available_seats(event_id)
            result = {"event_id": event_id, "available_seats": available_seats}
            return result
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении мест",
                extra={"event_id": event_id},
            )
            raise BusinessLogicError(
                "Неизвестная ошибка при получении мест", details={"reason": str(e)}
            )
