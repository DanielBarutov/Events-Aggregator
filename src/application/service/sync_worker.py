import asyncio
from collections.abc import Awaitable, Callable


from src.domain.exceptions import AppError, BusinessLogicError
from src.application.usecases.sync_events import SyncEventsUsecase
from src.infrastructure.db.session import AsyncSessionLocal
import logging

logger = logging.getLogger(__name__)


async def run_sync_loop(build_usecase: Callable[[], Awaitable[SyncEventsUsecase]]):
    try:
        while True:
            await asyncio.sleep(60)
            async with AsyncSessionLocal() as session:
                usecase = await build_usecase(session)
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
