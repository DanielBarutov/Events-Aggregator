from fastapi import APIRouter

from src.presentation.api.v1.health import router as health_router
from src.presentation.api.v1.events import router as events_router
from src.presentation.api.v1.tickets import router as tickets_router
from src.presentation.api.v1.sync import router as sync_router
from src.presentation.api.v1.metrics import router as metrics_router

router = APIRouter(prefix="/api")

router.include_router(health_router)
router.include_router(events_router)
router.include_router(tickets_router)
router.include_router(sync_router)
router.include_router(metrics_router)
