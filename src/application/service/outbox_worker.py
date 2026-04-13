import asyncio
from collections.abc import Awaitable, Callable

from src.domain.exceptions import AppError, BusinessLogicError
from src.application.usecases.create_ticket import OutboxUsecase
from src.infrastructure.db.session import AsyncSessionLocal

import logging


logger = logging.getLogger(__name__)


async def run_outbox_loop(build_usecase: Callable[[], Awaitable[OutboxUsecase]]):
    try:
        while True:
            await asyncio.sleep(30)
            async with AsyncSessionLocal() as session:
                logger.info(
                    "Начало выполнение проверки не отрпавленных сообщений Outbox"
                )
                usecase = await build_usecase(session)
                await usecase.execute()
    except AppError:
        raise
    except Exception as e:
        raise BusinessLogicError(
            "Неизвестная ошибка проверки Outbox",
            details={"reason": str(e)},
        )
