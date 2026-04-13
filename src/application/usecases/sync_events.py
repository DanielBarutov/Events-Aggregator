import datetime
import uuid as uuid_lib
import logging

from src.domain.exceptions import AppError, BusinessLogicError
from src.domain.models import SyncStatusEntity
from src.application.ports.repo.sync_events_repo import SyncEventsRepositoryPort
from src.application.ports.repo.get_events_repo import GetEventsRepositoryPort
from src.application.ports.event_provider_port import (
    EventProviderPort,
    EventMapperPort,
)


logger = logging.getLogger(__name__)


class SyncEventsUsecase:
    def __init__(
        self,
        client: EventProviderPort,
        mapper: EventMapperPort,
        sync_repository: SyncEventsRepositoryPort,
        events_repository: GetEventsRepositoryPort,
    ):
        self.client = client
        self.mapper = mapper
        self.sync_repository = sync_repository
        self.events_repository = events_repository
        self.uuid = str(uuid_lib.uuid4())
        self.max_changed_at = datetime.datetime(
            2000, 1, 1, tzinfo=datetime.timezone.utc
        )

    async def execute(self) -> None:
        try:
            last_sync: SyncStatusEntity = await self.get_sync()
            if last_sync.sync_status == "run":
                return
            self.max_changed_at = last_sync.last_changed_at.astimezone(
                datetime.timezone.utc
            )
            sync_start_changed_at = last_sync.last_changed_at.astimezone(
                datetime.timezone.utc
            )
            await self.start_sync()

            async for events in self.client.iter_events(
                last_sync.last_changed_at.strftime("%Y-%m-%d")
            ):
                for event in events:
                    event_changed_at = datetime.datetime.fromisoformat(
                        event.get("changed_at")
                    ).astimezone(datetime.timezone.utc)
                    if event_changed_at > sync_start_changed_at:
                        await self.events_repository.sync(
                            self.mapper.map_events(event),
                            self.mapper.map_places(event),
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

    async def start_sync(self) -> None:
        return await self.sync_repository.create(self.uuid, "run")

    async def get_sync(self) -> None:
        return await self.sync_repository.get()

    async def end(self) -> None:
        logger.info("Завершена синхранизация")
        return await self.sync_repository.update(
            self.uuid, "completed", self.max_changed_at
        )

    async def fail(self) -> None:
        return await self.sync_repository.update(self.uuid, "fail")
