from datetime import datetime, timezone
import uuid as uuid_lib
import logging


from src.domain.exceptions import AppError, BusinessLogicError
from src.domain.models import SyncStatusEntity
from src.infrastructure.utils.pagination import EventsPaginator
from src.infrastructure.clients.events_provider import EventsProviderClient
from src.infrastructure.mapper.events import EventsMapper


logger = logging.getLogger(__name__)


class SyncEventsUsecase:
    def __init__(
        self, client: EventsProviderClient, sync_repository, events_repository
    ):
        self.client = client
        self.sync_repository = sync_repository
        self.events_repository = events_repository
        self.uuid = str(uuid_lib.uuid4())
        self.max_changed_at = datetime(2000, 1, 1, tzinfo=timezone.utc)

    async def execute(self):
        try:
            last_sync: SyncStatusEntity = await self.get_sync()
            self.max_changed_at = last_sync.last_changed_at.astimezone(timezone.utc)
            sync_start_changed_at = last_sync.last_changed_at.astimezone(timezone.utc)
            await self.start_sync()
            paginator = EventsPaginator(
                self.client, last_sync.last_changed_at.strftime("%Y-%m-%d")
            )
            async for events in paginator:
                for event in events:
                    event_changed_at = datetime.fromisoformat(
                        event.get("changed_at")
                    ).astimezone(timezone.utc)
                    if event_changed_at > sync_start_changed_at:
                        await self.events_repository.sync(
                            EventsMapper(event).map_events(),
                            EventsMapper(event).map_places(),
                        )
                        self.max_changed_at = max(self.max_changed_at, event_changed_at)

        except AppError:
            await self.fail()
            logger.exception(
                "Фатальная ошибка при синхронизации", extra={"sync_id": self.uuid}
            )
            raise
        except Exception as e:
            await self.fail()
            logger.exception(
                "Неизвестая ошибка при синхронизации", extra={"sync_id": self.uuid}
            )
            raise BusinessLogicError(
                "Неизвестая ошибка при синхронизации", details={"reason": str(e)}
            )
        else:
            await self.end()

    async def start_sync(self):
        logger.info("Начата сихронизация")
        return await self.sync_repository.create(self.uuid, "run")

    async def get_sync(self):
        return await self.sync_repository.get()

    async def end(self):
        logger.info("Завершена синхранизация")
        return await self.sync_repository.update(
            self.uuid, "completed", self.max_changed_at
        )

    async def fail(self):
        return await self.sync_repository.update(self.uuid, "fail")
