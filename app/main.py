from contextlib import asynccontextmanager

import asyncio

from api.router import router
from fastapi import FastAPI

from service.sync_worker import run_sync_loop


class _SyncLoopUsecaseStub:
    async def execute(self, *_args, **_kwargs) -> None:
        pass


@asynccontextmanager
async def lifespan(_app: FastAPI):
    task = asyncio.create_task(run_sync_loop(_SyncLoopUsecaseStub()))
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(lifespan=lifespan)
app.include_router(router)
