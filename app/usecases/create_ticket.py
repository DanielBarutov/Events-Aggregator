from datetime import datetime
import logging

from infrastructure.repository.tickets import TicketsRepository
from infrastructure.clients.events_provider import EventsProviderClient
from infrastructure.repository.events import EventsRepository
from domain.models import UserEntity, EventEntity
from domain.exceptions import NotFoundError, ConflictError, AppError, BusinessLogicError


logger = logging.getLogger(__name__)


class TicketUsecase:
    def __init__(
        self,
        client: EventsProviderClient,
        event_repository: EventsRepository,
        tickets_repository: TicketsRepository,
    ):
        self.client = client
        self.event_repository = event_repository
        self.tickets_repository = tickets_repository

    async def create(
        self, event_id: str, first_name: str, last_name: str, email: str, seat: str
    ):
        try:
            available_seats = await self.client.get_available_seats(event_id)
            if seat not in available_seats:
                raise ConflictError("Место не доступно", details={"event_id": event_id})

            user: UserEntity = await self.tickets_repository.get_user(email)
            if not user:
                user = await self.tickets_repository.create_user(
                    email, first_name, last_name
                )
            event: EventEntity = await self.event_repository.get_event(event_id)
            if not event:
                raise NotFoundError(
                    "Событие не найдено", details={"event_id": event_id}
                )
            if event.status != "published":
                raise ConflictError(
                    "Событие не опубликовано", details={"event_id": event_id}
                )
            if event.registration_deadline < datetime.now(event.event_time.tzinfo):
                raise ConflictError(
                    "Событие уже началось", details={"event_id": event_id}
                )
            try:
                result = await self.client.create_ticket(
                    event_id, first_name, last_name, email, seat
                )
            except Exception:
                raise ConflictError(
                    "Место занято или вы уже зарегистрированны на это событие",
                    details={"event_id": event_id},
                )
            if result:
                await self.tickets_repository.create_ticket(
                    result.get("ticket_id"), user.id, event_id, seat
                )
                return result
            else:
                raise ConflictError(
                    "Не удалось создать тикет", details={"event_id": event_id}
                )
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при создании тикета",
                extra={"event_id": event_id},
            )
            raise BusinessLogicError(
                "Неизвестная ошибка при создании тикета", details={"reason": str(e)}
            )

    async def delete(self, ticket_id: str):
        try:
            event_data = await self.tickets_repository.get_ticket(ticket_id)
            event_id = event_data.event_id
            event: EventEntity = await self.event_repository.get_event(event_id)
            if event.status != "published":
                raise ConflictError(
                    "Событие не опубликовано", details={"event_id": event_id}
                )
            if event.event_time < datetime.now(event.event_time.tzinfo):
                raise ConflictError(
                    "Событие уже началось", details={"event_id": event_id}
                )
            await self.tickets_repository.delete_ticket(ticket_id)
            await self.client.delete_ticket(event_id, ticket_id)
            return {"success": True}
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при удалении тикета",
                extra={"ticket_id": ticket_id},
            )
            raise BusinessLogicError(
                "Неизвестная ошибка при удалении тикета", details={"reason": str(e)}
            )
