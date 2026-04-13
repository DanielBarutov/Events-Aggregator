import asyncio
from unittest.mock import AsyncMock, patch

from src.application.service.sync_worker import run_sync_loop


def test_run_sync_loop_builds_usecase_and_executes_once():
    async def run():
        usecase = AsyncMock()
        usecase.execute = AsyncMock(side_effect=SystemExit())
        build_usecase = AsyncMock(return_value=usecase)

        async def fast_sleep(_):
            return None

        with patch("src.application.service.sync_worker.asyncio.sleep", fast_sleep):
            try:
                await run_sync_loop(build_usecase)
            except SystemExit:
                pass

        assert build_usecase.await_count == 1
        usecase.execute.assert_awaited_once()

    asyncio.run(run())
