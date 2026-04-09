from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.presentation.deps import (
    get_event_by_id_usecase,
    get_event_seats_usecase,
    get_events_usecase,
)
from src.presentation.api.v1.events import router as events_router


def _event_payload(event_id: str = "e1"):
    return {
        "id": event_id,
        "name": "Demo Event",
        "place": {
            "id": "p1",
            "name": "Hall",
            "city": "Moscow",
            "address": "Main st",
            "seats_pattern": "A1,A2",
        },
        "event_time": datetime(2026, 4, 1, 10, 0, 0, tzinfo=timezone.utc),
        "registration_deadline": datetime(2026, 3, 31, 10, 0, 0, tzinfo=timezone.utc),
        "status": "published",
        "number_of_visitors": 10,
    }


def test_get_events_endpoint_uses_usecase_and_returns_page():
    class StubUsecase:
        async def execute(self, data_from):
            assert data_from is None
            return [_event_payload("e-list")]

    app = FastAPI()
    app.include_router(events_router, prefix="/api")
    app.dependency_overrides[get_events_usecase] = lambda: StubUsecase()

    client = TestClient(app)
    response = client.get("/api/events")

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["results"][0]["id"] == "e-list"


def test_get_event_by_id_endpoint_returns_single_event():
    class StubUsecase:
        async def execute(self, event_id):
            assert event_id == "e-id"
            return _event_payload(event_id)

    app = FastAPI()
    app.include_router(events_router, prefix="/api")
    app.dependency_overrides[get_event_by_id_usecase] = lambda: StubUsecase()

    client = TestClient(app)
    response = client.get("/api/events/e-id")

    assert response.status_code == 200
    assert response.json()["id"] == "e-id"


def test_get_event_seats_endpoint_returns_seats_payload():
    class StubUsecase:
        async def execute(self, event_id):
            return {"event_id": event_id, "available_seats": ["A1", "A2"]}

    app = FastAPI()
    app.include_router(events_router, prefix="/api")
    app.dependency_overrides[get_event_seats_usecase] = lambda: StubUsecase()

    client = TestClient(app)
    response = client.get("/api/events/e-seats/seats")

    assert response.status_code == 200
    assert response.json() == {"event_id": "e-seats", "available_seats": ["A1", "A2"]}
