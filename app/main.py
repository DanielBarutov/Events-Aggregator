from contextlib import asynccontextmanager
import asyncio
import logging
from dotenv import load_dotenv

from fastapi import FastAPI

from api.router import router
from api.exception_handlers import register_exception_handlers
from service.sync_worker import run_sync_loop

load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


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
register_exception_handlers(app)
app.include_router(router)
