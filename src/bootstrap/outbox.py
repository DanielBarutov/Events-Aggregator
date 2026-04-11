from collections.abc import Awaitable, Callable

from src.application.usecases.create_ticket import OutboxUsecase
from src.infrastructure.db.session import AsyncSessionLocal
from src.infrastructure.repository.tickets import TicketsRepository


def make_build_outbox_usecase() -> Callable[[], Awaitable[OutboxUsecase]]:
    async def build_outbox_usecase() -> OutboxUsecase:
        async with AsyncSessionLocal() as session:
            ticket_repository = TicketsRepository(session)
            return OutboxUsecase(ticket_repository)

    return build_outbox_usecase
