import asyncio
from collections.abc import Awaitable, Callable


from src.application.usecases.sync_events import SyncEventsUsecase
from src.infrastructure.db.session import AsyncSessionLocal
import logging

logger = logging.getLogger(__name__)


async def run_sync_loop(build_usecase: Callable[[], Awaitable[SyncEventsUsecase]]):
    while True:
        logger.info("Задача авто синхронизации запущена и будет выполнена через 60 сек")
        await asyncio.sleep(60)
        async with AsyncSessionLocal() as session:
            try:
                logger.info("Начата синхронизация ивентов ...")
                usecase = await build_usecase(session)
                await usecase.execute()
                await asyncio.sleep(86400)
            except Exception as e:
                logger.exception("Возникла ошибка при работе sync_worker", exc_info=e)
                await asyncio.sleep(5)
                continue
