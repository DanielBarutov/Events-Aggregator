"""
Тесты HTTP-эндпоинта синхронизации через TestClient (in-process, без реального сервера).
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.v1.sync import router as sync_router


def test_sync_endpoint_returns_ok():
    """
    GET /api/sync возвращает JSON со статусом ok.
    Роутер подключается с префиксом /api, как в основном приложении.
    """
    app = FastAPI()
    app.include_router(sync_router, prefix="/api")
    client = TestClient(app)
    response = client.get("/api/sync")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
