from src.domain.models import PlaceEntity, EventEntity
from src.infrastructure.clients.dto.events import EventDTO, PlaceDTO


class EventsMapper:
    def __init__(self) -> None:
        pass

    def map_events(self, event_list) -> EventEntity:
        event = EventDTO.model_validate(event_list)

        return EventEntity(
            id=event.id,
            name=event.name,
            place_id=event.place.id,
            event_time=event.event_time,
            registration_deadline=event.registration_deadline,
            status=event.status,
            number_of_visitors=event.number_of_visitors,
            status_changed_at=event.status_changed_at,
            changed_at=event.changed_at,
            created_at=event.created_at,
            place=PlaceEntity(
                id=event.place.id,
                name=event.place.name,
                city=event.place.city,
                address=event.place.address,
                seats_pattern=event.place.seats_pattern,
                changed_at=event.place.changed_at,
                created_at=event.place.created_at,
            )
            if event.place
            else None,
        )

    def map_places(self, event_list) -> PlaceEntity:
        place = PlaceDTO.model_validate(event_list["place"])
        return PlaceEntity(
            id=place.id,
            name=place.name,
            city=place.city,
            address=place.address,
            seats_pattern=place.seats_pattern,
            changed_at=place.changed_at,
            created_at=place.created_at,
        )
