import typing

from src.domain.models import (
    UserEntity,
    TicketEntity,
    IdempotencyKeysEntity,
)


class TicketsRepositoryPort(typing.Protocol):
    async def create_user(
        self, email: str, first_name: str, last_name: str
    ) -> UserEntity: ...

    async def create_ticket(
        self, ticket_id: str, user_id: str, event_id: str, seat: str, payload: dict
    ) -> TicketEntity: ...

    async def get_ticket(self, ticket_id: str) -> TicketEntity: ...

    async def get_user(self, email: str) -> UserEntity | None: ...

    async def delete_ticket(self, ticket_id: str) -> None: ...

    async def set_idempotency(
        self, idempotency_key: str, request_hash: str, ticket_id: str
    ) -> None: ...

    async def get_idempotency(self, idempotency_key: str) -> IdempotencyKeysEntity: ...
