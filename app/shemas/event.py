from datetime import datetime
from pydantic import BaseModel


class Place(BaseModel):
    id: str
    changed_at: datetime
    created_at: datetime
    name: str
    city: str
    address: str
    seats_pattern: str


class Event(BaseModel):
    id: str
    place: Place
    changed_at: datetime
    created_at: datetime
    name: str
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int
    status_changed_at: datetime
