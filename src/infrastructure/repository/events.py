from datetime import date
import uuid
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.domain.exceptions import DatabaseError, AppError, InputError, NotFoundError
from src.domain.models import EventEntity
from src.domain.models import PlaceEntity
from src.infrastructure.db.models import Event, Place
from src.infrastructure.repository.mappers.repo_mapper import ModelMapper


logger = logging.getLogger(__name__)


class EventsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.mapper = ModelMapper()

    async def get_event(self, event_id) -> EventEntity:
        try:
            try:
                uuid.UUID(str(event_id))
            except Exception:
                raise InputError(
                    "ID события не соотвествует формату", details={"event_id": event_id}
                )

            if event_id is None:
                raise NotFoundError(
                    "ID события не указан", details={"event_id": event_id}
                )

            result = await self.session.execute(
                select(Event)
                .where(Event.id == event_id)
                .join(Place)
                .options(selectinload(Event.place))
            )
            event = result.scalar()
            if event is None:
                raise NotFoundError(
                    "Событие не найдено", details={"event_id": event_id}
                )
            return self.mapper.to_event_entity(event)
        except AppError:
            raise
        except Exception:
            logger.exception("Неизвестная ошибка при получении события")
            raise NotFoundError("Событие не найдено", details={"event_id": event_id})

    async def get_events_with_places(
        self, date: date | None = None
    ) -> list[EventEntity]:
        try:
            if date is not None:
                req = select(Event).where(Event.event_time >= date)
            else:
                req = select(Event)
            result = await self.session.execute(
                req.join(Place).options(selectinload(Event.place))
            )
            events = result.scalars().all()

            return [self.mapper.to_event_entity(event) for event in events]
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении событий",
                extra={"date": date, "reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при получении событий", details={"reason": str(e)}
            )

    async def sync(self, event: EventEntity, place: PlaceEntity) -> None:
        try:
            if place is None or event is None:
                raise NotFoundError(
                    "Место или событие не найдены",
                    details={"place": place, "event": event},
                )
            m_place = self.mapper.to_place_model(place)
            m_event = self.mapper.to_event_model(event)
            await self.session.merge(m_place)
            await self.session.merge(m_event)
            await self.session.commit()
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при синхронизации",
                extra={"place": place, "event": event, "reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при синхронизации", details={"reason": str(e)}
            )

    async def count_events(self) -> int:
        try:
            count = await self.session.execute(select(func.count(Event.id)))
            result = count.scalar()
            return int(result) if result is not None else 0
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при подсчете событий",
                extra={"reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при подсчете событий", details={"reason": str(e)}
            )
