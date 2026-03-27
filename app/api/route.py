from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
