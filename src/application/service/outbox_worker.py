import asyncio
from collections.abc import Awaitable, Callable

from src.application.usecases.outbox import OutboxUsecase
from src.infrastructure.db.session import AsyncSessionLocal

import logging


logger = logging.getLogger(__name__)


async def run_outbox_loop(build_usecase: Callable[[], Awaitable[OutboxUsecase]]):
    logger.info(
        "Задача проверки не отправленных сообщений Outbox запущена и будет выполнена через 10 сек"
    )
    await asyncio.sleep(10)
    usecase = None
    while True:
        async with AsyncSessionLocal() as session:
            logger.info("Начата проверка не отправленных сообщений Outbox ...")
            try:
                usecase = await build_usecase(session)
                await usecase.execute()
                await asyncio.sleep(30)
            except Exception as e:
                logger.exception("Возникла ошибка при работе outbox_worker", exc_info=e)
                await asyncio.sleep(5)
                continue
