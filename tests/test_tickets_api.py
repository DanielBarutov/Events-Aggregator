from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.presentation.deps import get_tickets_usecase
from src.presentation.api.v1.tickets import router as tickets_router


def test_create_ticket_endpoint_passes_request_body_to_usecase():
    class StubUsecase:
        async def create(
            self, event_id, first_name, last_name, email, seat, idempotency_key
        ):
            assert event_id == "event-1"
            assert first_name == "Ivan"
            assert last_name == "Petrov"
            assert email == "ivan@test.com"
            assert seat == "A1"
            assert idempotency_key == "123456qwe"
            return {"ticket_id": "t-1"}

    app = FastAPI()
    app.include_router(tickets_router, prefix="/api")
    app.dependency_overrides[get_tickets_usecase] = lambda: StubUsecase()

    client = TestClient(app)
    response = client.post(
        "/api/tickets",
        json={
            "event_id": "event-1",
            "first_name": "Ivan",
            "last_name": "Petrov",
            "email": "ivan@test.com",
            "seat": "A1",
            "idempotency_key": "123456qwe",
        },
    )

    assert response.status_code == 201
    assert response.json() == {"ticket_id": "t-1"}


def test_delete_ticket_endpoint_delegates_to_usecase():
    class StubUsecase:
        async def delete(self, ticket_id):
            assert ticket_id == "t-42"
            return {"success": True}

    app = FastAPI()
    app.include_router(tickets_router, prefix="/api")
    app.dependency_overrides[get_tickets_usecase] = lambda: StubUsecase()

    client = TestClient(app)
    response = client.delete("/api/tickets/t-42")

    assert response.status_code == 200
    assert response.json() == {"success": True}
