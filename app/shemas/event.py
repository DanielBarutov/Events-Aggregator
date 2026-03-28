from datetime import datetime
from pydantic import BaseModel


class PlacePydantic(BaseModel):
    id: str
    name: str
    city: str
    address: str


class EventPydantic(BaseModel):
    id: str
    name: str
    place: PlacePydantic
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int


class EventListPydantic(BaseModel):
    results: list[EventPydantic]
    next: str | None = None
    previous: str | None = None


class EventPaginationPydantic(BaseModel):
    count: int
    next: str | None = None
    previous: str | None = None
    results: list[EventPydantic]
