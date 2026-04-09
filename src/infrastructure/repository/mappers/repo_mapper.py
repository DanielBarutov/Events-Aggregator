from src.domain.models import EventEntity
from src.domain.models import PlaceEntity
from src.infrastructure.db.models import Event, Place


class ModelMapper:
    def __init__(self) -> None:
        pass

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
            status=event.status.value,
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
            status=event.status.value,
            number_of_visitors=event.number_of_visitors,
            changed_at=event.changed_at,
            created_at=event.created_at,
            status_changed_at=event.status_changed_at,
        )
