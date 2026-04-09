from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.presentation.api.v1 import sync as sync_module
from src.presentation.api.v1.sync import router as sync_router


def test_sync_trigger_returns_202_and_success_json(monkeypatch):
    calls = {"scheduled": False}

    def fake_create_task(coro):
        calls["scheduled"] = True
        coro.close()
        return None

    monkeypatch.setattr(sync_module.asyncio, "create_task", fake_create_task)

    app = FastAPI()
    app.include_router(sync_router, prefix="/api")
    client = TestClient(app)

    response = client.post("/api/sync/trigger")

    assert response.status_code == 202
    assert response.json() == {"status": "Sync manual triggered successfully"}
    assert calls["scheduled"] is True
