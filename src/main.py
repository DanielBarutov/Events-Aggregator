import contextlib
import asyncio
import logging

from fastapi import FastAPI

from src.presentation.router import router
from src.presentation.exception_handlers import register_exception_handlers
from src.application.service.sync_worker import run_sync_loop
from src.bootstrap.sync import make_build_sync_usecase


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


build_sync_usecase = make_build_sync_usecase()


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI):
    task = asyncio.create_task(run_sync_loop(build_sync_usecase))
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
app.include_router(router)
