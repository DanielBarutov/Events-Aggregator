from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from repository.test_connection import TestConnectionRepository
from db.db import get_db

router = APIRouter(prefix="/api")


def get_test_connection_repo(session: AsyncSession = Depends(get_db)):
    return TestConnectionRepository(session)


@router.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


@router.get("/test-connection", tags=["test-connection"])
async def test_db(
    test_connection_repo: TestConnectionRepository = Depends(get_test_connection_repo),
):
    return await test_connection_repo.test_connection()
