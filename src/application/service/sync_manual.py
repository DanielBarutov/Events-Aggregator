import logging
from collections.abc import Awaitable, Callable

from src.domain.exceptions import AppError, BusinessLogicError
from src.application.usecases.sync_events import SyncEventsUsecase

logger = logging.getLogger(__name__)


async def run_manual_sync(
    build_usecase: Callable[[], Awaitable[SyncEventsUsecase]],
) -> SyncEventsUsecase:
    usecase = await build_usecase()
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
