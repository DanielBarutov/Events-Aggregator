import logging
from collections.abc import Awaitable, Callable

from src.application.usecases.sync_events import SyncEventsUsecase

logger = logging.getLogger(__name__)


async def run_manual_sync(
    build_usecase: Callable[[], Awaitable[SyncEventsUsecase]],
) -> SyncEventsUsecase:
    usecase = await build_usecase()
    try:
        await usecase.execute()
    except Exception:
        logger.exception("Manual sync background task failed")
