from fastapi import APIRouter
from api.v1.health import router as health_router
from api.v1.events import router as events_router
from api.v1.tickets import router as tickets_router
from api.v1.sync import router as sync_router

router = APIRouter(prefix="/api")

router.include_router(health_router)
router.include_router(events_router)
router.include_router(tickets_router)
router.include_router(sync_router)
