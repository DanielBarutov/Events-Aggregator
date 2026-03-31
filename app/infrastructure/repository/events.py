from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.domain.exceptions import DatabaseError, AppError
from infrastructure.db.models import Event, Place
from domain.models import EventEntity
from domain.models import PlaceEntity
from datetime import date
import logging

logger = logging.getLogger(__name__)


class EventsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def to_place_entity(self, place: Place) -> PlaceEntity:
        try:
            return PlaceEntity(
                id=place.id,
                name=place.name,
                city=place.city,
                address=place.address,
                seats_pattern=place.seats_pattern,
                changed_at=place.changed_at,
                created_at=place.created_at,
            )
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при преобразовании места",
                extra={"place": place},
                details={"reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при преобразовании места",
                details={"reason": str(e)},
            )

    def to_event_entity(self, event: Event) -> EventEntity:
        try:
            return EventEntity(
                id=event.id,
                name=event.name,
                place_id=event.place_id,
                place=self.to_place_entity(event.place),
                event_time=event.event_time,
                registration_deadline=event.registration_deadline,
                status=event.status,
                number_of_visitors=event.number_of_visitors,
                changed_at=event.changed_at,
                created_at=event.created_at,
                status_changed_at=event.status_changed_at,
            )
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при преобразовании события",
                extra={"event": event},
                details={"reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при преобразовании события",
                details={"reason": str(e)},
            )

    def to_place_model(self, place: PlaceEntity) -> Place:
        try:
            return Place(
                id=place.id,
                name=place.name,
                city=place.city,
                address=place.address,
                seats_pattern=place.seats_pattern,
                changed_at=place.changed_at,
                created_at=place.created_at,
            )
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при преобразовании места",
                extra={"place": place},
                details={"reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при преобразовании места",
                details={"reason": str(e)},
            )

    def to_event_model(self, event: EventEntity) -> Event:
        try:
            return Event(
                id=event.id,
                name=event.name,
                place_id=event.place_id,
                event_time=event.event_time,
                registration_deadline=event.registration_deadline,
                status=event.status,
                number_of_visitors=event.number_of_visitors,
                changed_at=event.changed_at,
                created_at=event.created_at,
                status_changed_at=event.status_changed_at,
            )
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при преобразовании события",
                extra={"event": event},
                details={"reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при преобразовании события",
                details={"reason": str(e)},
            )

    async def get_event(self, event_id) -> EventEntity:
        try:
            result = await self.session.execute(
                select(Event)
                .where(Event.id == event_id)
                .join(Place)
                .options(selectinload(Event.place))
            )
            event = result.scalar()
            return self.to_event_entity(event)
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении события",
                extra={"event_id": event_id},
                details={"reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при получении события", details={"reason": str(e)}
            )

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

            return [self.to_event_entity(event) for event in events]
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении событий",
                extra={"date": date},
                details={"reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при получении событий", details={"reason": str(e)}
            )

    async def get_place(self, event_id) -> EventEntity:
        try:
            result = await self.session.execute(
                select(Event)
                .where(Event.id == event_id, Event.status == "published")
                .join(Place)
                .options(selectinload(Event.place))
            )
            place = result.scalar().place
            return self.to_place_entity(place)
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении места",
                extra={"event_id": event_id},
                details={"reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при получении места", details={"reason": str(e)}
            )

    async def delete_events(self, events: list[EventEntity]):
        try:
            for event in events:
                await self.session.delete(event)
                await self.session.commit()
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при удалении событий",
                extra={"events": events},
                details={"reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при удалении событий", details={"reason": str(e)}
            )

    async def get_last_changed_at(self):
        try:
            result = await self.session.execute(
                select(Event.changed_at).order_by(Event.changed_at.desc()).limit(1)
            )
            return result.scalar()
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении последнего измененного времени",
                details={"reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при получении последнего измененного времени",
                details={"reason": str(e)},
            )

    async def sync(self, place: PlaceEntity, event: EventEntity) -> None:

        try:
            m_place = self.to_place_model(place)
            m_event = self.to_event_model(event)
            await self.session.merge(m_place)
            await self.session.merge(m_event)
            await self.session.commit()
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при синхронизации",
                extra={"place": place, "event": event},
                details={"reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при синхронизации", details={"reason": str(e)}
            )
