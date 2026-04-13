import logging
import asyncio
from collections.abc import Awaitable, Callable

from src.domain.exceptions import AppError, BusinessLogicError
from src.application.usecases.sync_events import SyncEventsUsecase
from src.infrastructure.db.session import AsyncSessionLocal

logger = logging.getLogger(__name__)
sync_lock = asyncio.Lock()


async def run_manual_sync(
    build_usecase: Callable[[], Awaitable[SyncEventsUsecase]],
) -> SyncEventsUsecase:
    if sync_lock.locked():
        return
    async with sync_lock:
        async with AsyncSessionLocal() as session:
            usecase = await build_usecase(session)
            try:
                await usecase.execute()
            except AppError:
                raise
            except Exception as e:
                logger.exception(
                    "Неизвестная ошибка ручной задачи при синхронизации",
                    extra={"usecase": usecase},
                )
                raise BusinessLogicError(
                    "Неизвестная ошибка ручной задачи при синхронизации",
                    details={"reason": str(e)},
                )
