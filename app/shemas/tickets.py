from pydantic import BaseModel


class TicketCreateResponse(BaseModel):
    ticket_id: str


class TicketDeleteResponse(BaseModel):
    success: bool
