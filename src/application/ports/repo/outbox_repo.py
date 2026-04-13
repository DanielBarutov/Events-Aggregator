import typing

from src.domain.models import OutboxEntity


class OutboxRepositoryPort(typing.Protocol):
    async def get_outbox(self) -> list[OutboxEntity] | None: ...

    async def add_retry(self, outbox_id: str) -> None: ...

    async def change_outbox_status(self, outbox_id: str, status: str) -> None: ...
