from domain.models import PlaceEntity, EventEntity
from shemas.sync import SyncEventPydantic, SyncPlacePydantic


class EventsMapper:
    def __init__(self, event_list):
        self.event_list = event_list

    def map_events(self) -> list[EventEntity]:
        events = [SyncEventPydantic.model_validate(event) for event in self.event_list]
        return [
            EventEntity(
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
            for event in events
        ]

    def map_places(self) -> list[PlaceEntity]:
        places = [
            SyncPlacePydantic.model_validate(event["place"])
            for event in self.event_list
        ]
        return [
            PlaceEntity(
                id=place.id,
                name=place.name,
                city=place.city,
                address=place.address,
                seats_pattern=place.seats_pattern,
                changed_at=place.changed_at,
                created_at=place.created_at,
            )
            for place in places
        ]
