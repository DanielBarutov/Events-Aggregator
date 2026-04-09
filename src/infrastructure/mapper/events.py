import logging

from src.domain.models import PlaceEntity, EventEntity
from src.domain.exceptions import AppError, DatabaseError
from src.shemas.sync import SyncEventPydantic, SyncPlacePydantic


logger = logging.getLogger(__name__)


class EventsMapper:
    def __init__(self, event_list):
        self.event_list = event_list

    def map_events(self) -> EventEntity:
        try:
            event = SyncEventPydantic.model_validate(self.event_list)
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
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при преобразовании события",
                extra={"event": event, "reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при преобразовании события",
                details={"reason": str(e)},
            )

    def map_places(self) -> PlaceEntity:
        try:
            place = SyncPlacePydantic.model_validate(self.event_list["place"])
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
                "Неизвестная ошика при преобразовании места",
                extra={"place": place, "reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошика при преобразовании места",
                details={"reason": str(e)},
            )
