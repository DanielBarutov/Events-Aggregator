from datetime import datetime

from pydantic import BaseModel


class SyncPlacePydantic(BaseModel):
    id: str
    name: str
    city: str
    address: str
    seats_pattern: str
    changed_at: datetime
    created_at: datetime


class SyncEventPydantic(BaseModel):
    id: str
    name: str
    place: SyncPlacePydantic
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int
    changed_at: datetime
    created_at: datetime
    status_changed_at: datetime
