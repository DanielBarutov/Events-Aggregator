from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EventStatus(Enum):
    NEW = "new"
    PUBLISHED = "published"
    REGISTRATION_CLOSED = "registration_closed"
    FINISHED = "finished"

    @classmethod
    def from_string(cls, value: str) -> "EventStatus":
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(f"Invalid event status: {value}")

    def to_string(self) -> str:
        return self.value


class SyncStatus(Enum):
    COMPLETED = "completed"
    RUN = "run"
    FAIL = "fail"


@dataclass
class PlaceEntity:
    id: str
    name: str
    city: str
    address: str
    seats_pattern: str
    changed_at: datetime
    created_at: datetime


@dataclass
class EventEntity:
    id: str
    name: str
    place_id: str
    place: PlaceEntity
    event_time: datetime
    registration_deadline: datetime
    status: EventStatus
    number_of_visitors: int
    changed_at: datetime
    created_at: datetime
    status_changed_at: datetime


@dataclass
class SyncStatusEntity:
    id: str
    last_sync_time: datetime
    last_changed_at: datetime
    sync_status: SyncStatus


@dataclass
class UserEntity:
    id: str
    email: str
    first_name: str
    last_name: str
    created_at: datetime


@dataclass
class TicketEntity:
    id: str
    user_id: str
    event_id: str
    seat: str
    created_at: datetime
