from pydantic import BaseModel


class TicketCreateRequest(BaseModel):
    event_id: str
    first_name: str
    last_name: str
    email: str
    seat: str
    idempotency_key: str | None = None


class TicketDeleteResponse(BaseModel):
    success: bool
