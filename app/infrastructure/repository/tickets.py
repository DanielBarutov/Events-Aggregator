from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.models import User, Ticket
from domain.models import TicketEntity, UserEntity
import uuid
from datetime import datetime
from domain.exceptions import DatabaseError, AppError, NotFoundError
import logging

logger = logging.getLogger(__name__)


class TicketsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(
        self, email: str, first_name: str, last_name: str
    ) -> UserEntity:
        try:
            if email is None:
                raise NotFoundError("Email не указан", details={"email": email})
            if first_name is None:
                raise NotFoundError(
                    "Имя не указано", details={"first_name": first_name}
                )
            if last_name is None:
                raise NotFoundError(
                    "Фамилия не указана", details={"last_name": last_name}
                )
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
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при создании пользователя",
                extra={"email": email, "reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при создании пользователя",
                details={"reason": str(e)},
            )

    async def create_ticket(
        self, ticket_id: str, user_id: str, event_id: str, seat: str
    ) -> TicketEntity:
        try:
            if ticket_id is None:
                raise NotFoundError(
                    "ID тикета не указан", details={"ticket_id": ticket_id}
                )
            if user_id is None:
                raise NotFoundError(
                    "ID пользователя не указан", details={"user_id": user_id}
                )
            if event_id is None:
                raise NotFoundError(
                    "ID события не указан", details={"event_id": event_id}
                )
            if seat is None:
                raise NotFoundError("Место не указано", details={"seat": seat})
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
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при создании тикета",
                extra={"ticket_id": ticket_id, "reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при создании тикета", details={"reason": str(e)}
            )

    async def get_ticket(self, ticket_id: str) -> TicketEntity:
        try:
            if ticket_id is None:
                raise NotFoundError(
                    "ID тикета не указан", details={"ticket_id": ticket_id}
                )
            data = await self.session.execute(
                select(Ticket).where(Ticket.id == ticket_id)
            )
            ticket = data.scalar()
            if not ticket:
                raise NotFoundError("Тикет не найден", details={"ticket_id": ticket_id})
            return TicketEntity(
                id=ticket.id,
                user_id=ticket.user_id,
                event_id=ticket.event_id,
                seat=ticket.seat,
                created_at=ticket.created_at,
            )
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении тикета",
                extra={"ticket_id": ticket_id, "reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при получении тикета", details={"reason": str(e)}
            )

    async def get_user(self, email: str) -> UserEntity | None:
        try:
            if email is None:
                raise NotFoundError("Email не указан", details={"email": email})
            data = await self.session.execute(select(User).where(User.email == email))
            user = data.scalar()
            if user is None:
                return None
            return UserEntity(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                created_at=user.created_at,
            )
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении пользователя",
                extra={"email": email, "reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при получении пользователя",
                details={"reason": str(e)},
            )

    async def delete_ticket(self, ticket_id: str) -> None:
        try:
            if ticket_id is None:
                raise NotFoundError(
                    "ID тикета не указан", details={"ticket_id": ticket_id}
                )
            data = await self.session.execute(
                select(Ticket).where(Ticket.id == ticket_id)
            )
            ticket = data.scalar()
            if not ticket:
                raise NotFoundError("Тикет не найден", details={"ticket_id": ticket_id})
            await self.session.delete(ticket)
            await self.session.commit()
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при удалении тикета",
                extra={"ticket_id": ticket_id, "reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при удалении тикета", details={"reason": str(e)}
            )
