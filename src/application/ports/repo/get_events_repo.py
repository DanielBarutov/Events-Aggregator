import typing
import datetime

from src.domain.models import EventEntity, PlaceEntity


class GetEventsRepositoryPort(typing.Protocol):
    async def get_events_with_places(
        self, data_from: datetime.date | None = None
    ) -> list[EventEntity]: ...

    async def get_event(self, event_id: str) -> EventEntity: ...
    async def sync(self, event: EventEntity, place: PlaceEntity) -> None: ...
