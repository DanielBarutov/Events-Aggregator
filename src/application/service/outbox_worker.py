import asyncio
from collections.abc import Awaitable, Callable

from src.domain.exceptions import AppError, BusinessLogicError
from src.application.usecases.create_ticket import OutboxUsecase
from src.infrastructure.db.session import AsyncSessionLocal

import logging


logger = logging.getLogger(__name__)


async def run_outbox_loop(build_usecase: Callable[[], Awaitable[OutboxUsecase]]):
    while True:
        async with AsyncSessionLocal() as session:
            logger.info(
                "Задача проверки не отправленных сообщений Outbox запущена и будет выполнена через 10 сек"
            )
            await asyncio.sleep(10)
            logger.info("Начало выполнение проверки не отправленных сообщений Outbox")
            try:
                usecase = await build_usecase(session)
                await usecase.execute()
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
