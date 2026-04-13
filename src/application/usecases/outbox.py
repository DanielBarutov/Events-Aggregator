import logging

from src.application.ports.repo.outbox_repo import OutboxRepositoryPort
from src.application.ports.outbox_provider_port import OutboxProviderPort
from src.domain.models import OutboxEntity

logger = logging.getLogger(__name__)


class OutboxUsecase:
    def __init__(
        self, repository: OutboxRepositoryPort, client: OutboxProviderPort
    ) -> None:
        self.repository = repository
        self.client = client

    async def execute(self):
        result: list[OutboxEntity] = await self.repository.get_outbox()
        if result is None:
            logger.info("Необработанных сообщений нет ...")
            return
        for i in result:
            try:
                response = None
                if i.retry <= 3:
                    await self.repository.add_retry(i.id)
                    response = await self.client.execute(i.payload)
                    await self.repository.change_outbox_status(i.id, "sent")
                else:
                    await self.repository.change_outbox_status(i.id, "fail")
                if response:
                    logger.info(f"Сообщение с id: {i.id} в Capushino было доставлено!")
            except Exception as e:
                logger.exception("Ошибка при обработке сообщений из Outbox")
                raise e
