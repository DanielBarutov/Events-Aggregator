from dataclasses import dataclass
from datetime import datetime


@dataclass
class Place:
    id: str
    name: str
    city: str
    address: str
    seats_pattern: str
    created_at: datetime
    changed_at: datetime


@dataclass
class Event:
    id: str
    place_id: str
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int
    created_at: datetime
    changed_at: datetime
    status_changed_at: datetime
