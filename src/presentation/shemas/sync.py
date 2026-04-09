import datetime

from pydantic import BaseModel


class SyncPlacePydantic(BaseModel):
    id: str
    name: str
    city: str
    address: str
    seats_pattern: str
    changed_at: datetime.datetime
    created_at: datetime.datetime


class SyncEventPydantic(BaseModel):
    id: str
    name: str
    place: SyncPlacePydantic
    event_time: datetime.datetime
    registration_deadline: datetime.datetime
    status: str
    number_of_visitors: int
    changed_at: datetime.datetime
    created_at: datetime.datetime
    status_changed_at: datetime.datetime
