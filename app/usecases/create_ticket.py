from datetime import datetime
from infrastructure.repository.tickets import TicketsRepository
from infrastructure.clients.events_provider import EventsProviderClient
from infrastructure.repository.events import EventsRepository
from domain.models import UserEntity, EventEntity


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
        available_seats = await self.client.get_available_seats(event_id)
        if seat not in available_seats:
            raise Exception("Seat not available")

        user: UserEntity = await self.tickets_repository.get_user(email)
        if not user:
            user = await self.tickets_repository.create_user(
                email, first_name, last_name
            )
        event: EventEntity = await self.event_repository.get_event(event_id)
        if not event:
            raise Exception("Event not found")
        if event.status != "published":
            raise Exception("Event is not published")
        if event.registration_deadline < datetime.now(event.event_time.tzinfo):
            raise Exception("Event has already started")
        try:
            result = self.client.create_ticket(
                event_id, first_name, last_name, email, seat
            )
        except Exception:
            raise Exception("Место занято или вы уже зарегистрированны на это событие")
        if result:
            await self.tickets_repository.create_ticket(
                result.get("ticket_id"), user.id, event_id, seat
            )
            return result
        else:
            raise Exception("Failed to create ticket")

    async def delete(self, ticket_id: str):
        event_data = await self.tickets_repository.get_ticket(ticket_id)
        event_id = event_data.event_id
        event: EventEntity = await self.event_repository.get_event(event_id)
        if event.status != "published":
            raise Exception("Event is not published")
        if event.event_time < datetime.now(event.event_time.tzinfo):
            raise Exception("Event has already started")
        self.client.delete_ticket(event_id, ticket_id)
        await self.tickets_repository.delete_ticket(ticket_id)
