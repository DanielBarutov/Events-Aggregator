import dataclasses
import datetime
import enum
import json


class EventStatus(enum.Enum):
    new = "new"
    published = "published"
    registration_closed = "registration_closed"
    finished = "finished"

    @classmethod
    def from_string(cls, value: str) -> "EventStatus":
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(f"Invalid event status: {value}")

    def to_string(self) -> str:
        return self.value


class SyncStatus(enum.Enum):
    completed = "completed"
    run = "run"
    fail = "fail"


class OutboxTypeEvent(enum.Enum):
    buying = "buying"


class OutboxStatus(enum.Enum):
    awaits = "awaits"
    sent = "sent"


@dataclasses.dataclass
class PlaceEntity:
    id: str
    name: str
    city: str
    address: str
    seats_pattern: str
    changed_at: datetime.datetime
    created_at: datetime.datetime


@dataclasses.dataclass
class EventEntity:
    id: str
    name: str
    place_id: str
    place: PlaceEntity
    event_time: datetime.datetime
    registration_deadline: datetime.datetime
    status: EventStatus
    number_of_visitors: int
    changed_at: datetime.datetime
    created_at: datetime.datetime
    status_changed_at: datetime.datetime


@dataclasses.dataclass
class SyncStatusEntity:
    id: str
    last_sync_time: datetime.datetime
    last_changed_at: datetime.datetime
    sync_status: SyncStatus


@dataclasses.dataclass
class UserEntity:
    id: str
    email: str
    first_name: str
    last_name: str
    created_at: datetime.datetime


@dataclasses.dataclass
class TicketEntity:
    id: str
    user_id: str
    event_id: str
    seat: str
    created_at: datetime.datetime


@dataclasses.dataclass
class OutboxEntity:
    id: str
    type_event: OutboxTypeEvent
    payload: json
    status: OutboxStatus
    created_at: datetime.datetime


@dataclasses.dataclass
class IdempotencyKeysEntity:
    id: int
    key: str
    request_hash: str
    ticket_id: str
    created_at: datetime.datetime
