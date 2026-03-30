from httpx import request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from infrastructure.db.models import Event, Place
from datetime import date


class EventsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_event(self, event_id) -> Event:
        result = await self.session.execute(
            select(Event)
            .where(Event.id == event_id)
            .join(Place)
            .options(selectinload(Event.place))
        )
        return result.scalar()

    async def get_events_with_places(self, date: date | None = None) -> list[Event]:
        if date is not None:
            req = select(Event).where(Event.event_time >= date)
        else:
            req = select(Event)
        result = await self.session.execute(
            req.join(Place).options(selectinload(Event.place))
        )
        return list(result.scalars().all())

    async def get_event_seats(self, event_id) -> Event:
        result = await self.session.execute(
            select(Event)
            .where(Event.id == event_id, Event.status == "published")
            .join(Place)
            .options(selectinload(Event.place))
        )
        data = result.scalar().place
        return data  # На завтра Дальше с ним отработать и создать ручку

    async def get_locked_seats(self, event_id):
        result = await self.session.execute(
            select(Event.seats).where(Event.id == event_id)
        )
        return result.scalar()

    async def delete_events(self, events: list[Event]):
        for event in events:
            await self.session.delete(event)
        await self.session.commit()

    async def get_last_changed_at(self):
        result = await self.session.execute(
            select(Event.changed_at).order_by(Event.changed_at.desc()).limit(1)
        )
        return result.scalar()

    async def upsert_places_and_events(
        self, places: list[Place], events: list[Event]
    ) -> None:
        for p in places:
            await self.session.merge(p)
        for e in events:
            await self.session.merge(e)
        await self.session.commit()
