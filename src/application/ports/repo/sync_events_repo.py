import typing
import datetime

from src.domain.models import SyncStatusEntity


class SyncEventsRepositoryPort(typing.Protocol):
    async def create(self, uuid: str, sync_status: str) -> None: ...
    async def get(self) -> SyncStatusEntity: ...
    async def update(
        self, uuid: str, sync_status: str, changed_at: datetime.datetime.now()
    ) -> None: ...
