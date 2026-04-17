import contextlib
import asyncio
import logging

from fastapi import FastAPI
import sentry_sdk

import src.setting
from src.presentation.router import router, router_metrics
from src.presentation.exception_handlers import register_exception_handlers
from src.application.service.sync_worker import run_sync_loop
from src.application.service.outbox_worker import run_outbox_loop
from src.bootstrap.sync import make_build_sync_usecase
from src.bootstrap.outbox import make_build_outbox_usecase
from src.presentation.middlewares.metrics import metrics_middleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

sentry_sdk.init(
    dsn=src.setting.SENTRY_DSN,
    traces_sample_rate=1.0,
)

build_sync_usecase = make_build_sync_usecase()
build_outbox_usecase = make_build_outbox_usecase()


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI):
    task_outbox = asyncio.create_task(run_outbox_loop(build_outbox_usecase))
    task_sync = asyncio.create_task(run_sync_loop(build_sync_usecase))
    try:
        yield
    finally:
        task_sync.cancel()
        task_outbox.cancel()
        try:
            await task_sync
            await task_outbox
        except asyncio.CancelledError:
            pass


app = FastAPI(lifespan=lifespan)
app.middleware("http")(metrics_middleware)
register_exception_handlers(app)
app.include_router(router)
app.include_router(router_metrics)
