from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.deps import manual_trigger_sync
from src.api.v1.sync import router as sync_router


def test_sync_trigger_returns_success_json():
    class StubUsecase:
        async def execute(self):
            return None

    app = FastAPI()
    app.include_router(sync_router, prefix="/api")
    app.dependency_overrides[manual_trigger_sync] = lambda: StubUsecase()

    client = TestClient(app)
    response = client.post("/api/sync/trigger")

    assert response.status_code == 200
    assert response.json() == {"status": "sync manual triggered successfully"}
