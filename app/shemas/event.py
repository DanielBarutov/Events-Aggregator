from datetime import datetime
import uuid
from zoneinfo import ZoneInfo
from pydantic import BaseModel, ConfigDict, field_validator

MSK_TZ = ZoneInfo("Europe/Moscow")


class PlacePydantic(BaseModel):
    id: str
    name: str
    city: str
    address: str
    seats_pattern: str


class EventPydantic(BaseModel):
    id: str
    name: str
    place: PlacePydantic
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int

    model_config = ConfigDict(from_attributes=True)

    @field_validator("event_time", "registration_deadline", mode="before")
    @classmethod
    def format_to_msk(cls, v):
        return v.astimezone(MSK_TZ).strftime("%Y-%m-%dT%H:%M:%S")


class EventListPydantic(BaseModel):
    results: list[EventPydantic]
    next: str | None = None
    previous: str | None = None


class EventPaginationPydantic(BaseModel):
    count: int
    next: str | None = None
    previous: str | None = None
    results: list[EventPydantic]


class EventAvaibleSeats:
    event_id: uuid
