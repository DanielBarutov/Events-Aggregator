from collections.abc import Awaitable, Callable

import src.setting
from src.application.usecases.outbox import OutboxUsecase
from src.infrastructure.clients.outbox_provider import OutboxProviderClient
from src.infrastructure.repository.outbox import OutboxRepository


def make_build_outbox_usecase() -> Callable[[], Awaitable[OutboxUsecase]]:
    async def build_outbox_usecase(session) -> OutboxUsecase:
        repository = OutboxRepository(session)
        client = OutboxProviderClient(
            src.setting.NOTIFY_PRIVIDER_SERVER,
            src.setting.EVENTS_PROVIDER_API_KEY,
        )
        return OutboxUsecase(repository, client)

    return build_outbox_usecase
