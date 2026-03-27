from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from repository.test_connection import test_connection
from db.db import get_db

router = APIRouter(prefix="/api")


@router.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


@router.get("/test-connection", tags=["test-connection"])
def test_db(db: Session = Depends(get_db)):
    return test_connection()
