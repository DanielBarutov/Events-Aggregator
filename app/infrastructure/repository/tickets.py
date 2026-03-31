from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.models import User, Ticket
from domain.models import TicketEntity, UserEntity
import uuid
from datetime import datetime


class TicketsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(
        self, email: str, first_name: str, last_name: str
    ) -> UserEntity:
        id = str(uuid.uuid4())
        created_at = datetime.now()
        self.session.add(
            User(
                id=id,
                email=email,
                first_name=first_name,
                last_name=last_name,
                created_at=created_at,
            )
        )
        await self.session.commit()
        return UserEntity(
            id=id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            created_at=created_at,
        )

    async def create_ticket(
        self, ticket_id: str, user_id: str, event_id: str, seat: str
    ) -> TicketEntity:
        created_at = datetime.now()
        self.session.add(
            Ticket(
                id=ticket_id,
                user_id=user_id,
                event_id=event_id,
                seat=seat,
                created_at=created_at,
            )
        )
        await self.session.commit()
        return TicketEntity(
            id=ticket_id,
            user_id=user_id,
            event_id=event_id,
            seat=seat,
            created_at=created_at,
        )

    async def get_ticket(self, ticket_id: str) -> TicketEntity:
        data = await self.session.execute(select(Ticket).where(Ticket.id == ticket_id))
        ticket = data.scalar()

        return TicketEntity(
            id=ticket.id,
            user_id=ticket.user_id,
            event_id=ticket.event_id,
            seat=ticket.seat,
            created_at=ticket.created_at,
        )

    async def get_user(self, email: str) -> UserEntity:
        data = await self.session.execute(select(User).where(User.email == email))
        user = data.scalar()
        if not user:
            return None
        return UserEntity(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=user.created_at,
        )

    async def delete_ticket(self, ticket_id: str) -> None:
        data = await self.session.execute(select(Ticket).where(Ticket.id == ticket_id))
        ticket = data.scalar()
        if not ticket:
            raise Exception("Ticket not found")
        await self.session.delete(ticket)
        await self.session.commit()
