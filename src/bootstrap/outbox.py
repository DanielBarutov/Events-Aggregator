from collections.abc import Awaitable, Callable

import src.setting
from src.application.usecases.create_ticket import OutboxUsecase
from src.infrastructure.clients.outbox_provider import OutboxProviderClient
from src.infrastructure.db.session import AsyncSessionLocal
from src.infrastructure.repository.tickets import TicketsRepository


def make_build_outbox_usecase() -> Callable[[], Awaitable[OutboxUsecase]]:
    async def build_outbox_usecase(session) -> OutboxUsecase:
        async with AsyncSessionLocal() as session:
            repository = TicketsRepository(session)
            client = OutboxProviderClient(
                src.setting.EVENTS_PROVIDER_SERVER,
                src.setting.EVENTS_PROVIDER_API_KEY,
            )
            return OutboxUsecase(repository, client)

    return build_outbox_usecase
