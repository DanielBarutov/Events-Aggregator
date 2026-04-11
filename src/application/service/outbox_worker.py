import asyncio
from collections.abc import Awaitable, Callable

from src.domain.exceptions import AppError, BusinessLogicError
from src.application.usecases.create_ticket import OutboxUsecase


import logging


logger = logging.getLogger(__name__)


async def run_outbox_loop(build_usecase: Callable[[], Awaitable[OutboxUsecase]]):
    try:
        while True:
            await asyncio.sleep(2)
            usecase = await build_usecase()
            await usecase.execute()
            await asyncio.sleep(60)
    except AppError:
        raise
    except Exception as e:
        logger.exception(
            "Неизвестная ошибка проверки Outbox",
            extra={"usecase": usecase},
        )
        raise BusinessLogicError(
            "Неизвестная ошибка проверки Outbox",
            details={"reason": str(e)},
        )
