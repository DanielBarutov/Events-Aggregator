from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from infrastructure.db.models import Event, Place
from domain.models import EventEntity
from domain.models import PlaceEntity
from datetime import date


class EventsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def to_place_entity(self, place: Place) -> PlaceEntity:
        return PlaceEntity(
            id=place.id,
            name=place.name,
            city=place.city,
            address=place.address,
            seats_pattern=place.seats_pattern,
            changed_at=place.changed_at,
            created_at=place.created_at,
        )

    def to_event_entity(self, event: Event) -> EventEntity:
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

    def to_place_model(self, place: PlaceEntity) -> Place:
        return Place(
            id=place.id,
            name=place.name,
            city=place.city,
            address=place.address,
            seats_pattern=place.seats_pattern,
            changed_at=place.changed_at,
            created_at=place.created_at,
        )

    def to_event_model(self, event: EventEntity) -> Event:
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

    async def get_event(self, event_id) -> EventEntity:
        result = await self.session.execute(
            select(Event)
            .where(Event.id == event_id)
            .join(Place)
            .options(selectinload(Event.place))
        )
        event = result.scalar()
        return self.to_event_entity(event)

    async def get_events_with_places(
        self, date: date | None = None
    ) -> list[EventEntity]:
        if date is not None:
            req = select(Event).where(Event.event_time >= date)
        else:
            req = select(Event)
        result = await self.session.execute(
            req.join(Place).options(selectinload(Event.place))
        )
        events = result.scalars().all()

        return [self.to_event_entity(event) for event in events]

    async def get_place(self, event_id) -> EventEntity:
        result = await self.session.execute(
            select(Event)
            .where(Event.id == event_id, Event.status == "published")
            .join(Place)
            .options(selectinload(Event.place))
        )
        place = result.scalar().place
        return self.to_place_entity(place)

    async def delete_events(self, events: list[EventEntity]):
        for event in events:
            await self.session.delete(event)
        await self.session.commit()

    async def get_last_changed_at(self):
        result = await self.session.execute(
            select(Event.changed_at).order_by(Event.changed_at.desc()).limit(1)
        )
        return result.scalar()

    async def sync(self, places: list[PlaceEntity], events: list[EventEntity]) -> None:
        print(places)
        m_places = [self.to_place_model(place) for place in places]
        m_events = [self.to_event_model(event) for event in events]
        for p in m_places:
            await self.session.merge(p)
        for e in m_events:
            await self.session.merge(e)
        await self.session.commit()
