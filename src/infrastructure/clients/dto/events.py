import datetime
import enum
import pydantic


class Status(enum.Enum):
    new = "new"
    published = "published"
    registration_closed = "registration_closed"
    finished = "finished"


class PlaceDTO(pydantic.BaseModel):
    id: str
    name: str
    city: str
    address: str
    seats_pattern: str
    changed_at: datetime.datetime
    created_at: datetime.datetime


class EventDTO(pydantic.BaseModel):
    id: str
    name: str
    event_time: datetime.datetime
    registration_deadline: datetime.datetime
    status: Status
    number_of_visitors: int
    status_changed_at: datetime.datetime
    changed_at: datetime.datetime
    created_at: datetime.datetime
    place: PlaceDTO | None


class EventListDTO(pydantic.BaseModel):
    results: list[EventDTO]
    next: str | None = None
    previous: str | None = None
