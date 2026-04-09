import asyncio

from src.domain.exceptions import AppError, BusinessLogicError
from src.infrastructure.repository.sync import SyncMetadataRepository
from src.infrastructure.repository.events import EventsRepository
from src.infrastructure.clients.events_provider import EventsProviderClient
from src.infrastructure.db.session import AsyncSessionLocal
from src.application.usecases.sync_events import SyncEventsUsecase

import logging

logger = logging.getLogger(__name__)


async def run_sync_loop(usecase):
    try:
        while True:
            await asyncio.sleep(300)
            async with AsyncSessionLocal() as session:
                sync_repo = SyncMetadataRepository(session)
                events_repo = EventsRepository(session)
                usecase = SyncEventsUsecase(
                    EventsProviderClient(), sync_repo, events_repo
                )
                await usecase.execute()
            await asyncio.sleep(86390)
    except AppError:
        raise
    except Exception as e:
        logger.exception(
            "Неизвестная ошибка асинхронной задачи при синхронизации",
            extra={"usecase": usecase},
        )
        raise BusinessLogicError(
            "Неизвестная ошибка асинхронной задачи при синхронизации",
            details={"reason": str(e)},
        )
