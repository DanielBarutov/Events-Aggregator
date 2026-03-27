from fastapi import APIRouter
from repository.test_connection import test_connection

router = APIRouter(prefix="/api")


@router.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


@router.get("/test-connection", tags=["test-connection"])
def test_db():
    return test_connection()
