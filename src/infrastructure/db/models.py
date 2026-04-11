import datetime
import enum
import zoneinfo
import uuid

from sqlalchemy import JSON, String, Integer, ForeignKey, Column, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase, relationship


timezone_msk = zoneinfo.ZoneInfo("Europe/Moscow")


class SyncStatus(enum.Enum):
    completed = "completed"
    run = "run"
    fail = "fail"


class EventStatus(enum.Enum):
    new = "new"
    published = "published"
    registration_closed = "registration_closed"
    finished = "finished"


class TypeEvent(enum.Enum):
    buying = "buying"


class OutboxStatus(enum.Enum):
    awaits = "awaits"
    sent = "sent"


class Base(DeclarativeBase):
    pass


class Place(Base):
    __tablename__ = "places"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)
    seats_pattern = Column(String, nullable=True)
    changed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )
    events = relationship("Event", back_populates="place")


class Event(Base):
    __tablename__ = "events"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    place_id = Column(String, ForeignKey("places.id"), nullable=False)
    place = relationship("Place", foreign_keys=[place_id], back_populates="events")
    event_time = Column(
        DateTime(timezone=True),
        nullable=False,
    )
    registration_deadline = Column(
        DateTime(timezone=True),
        nullable=False,
    )
    status = Column(Enum(EventStatus), nullable=True)
    number_of_visitors = Column(Integer, nullable=True)
    changed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )
    status_changed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )


class SyncStatus(Base):
    __tablename__ = "sync_status"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    last_sync_time = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.now(timezone_msk),
    )
    last_changed_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.now(timezone_msk),
    )
    sync_status = Column(Enum(SyncStatus), nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    tickets = relationship("Ticket", back_populates="user")
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.now(timezone_msk),
    )


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    seat = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.now(timezone_msk),
    )
    user = relationship("User", foreign_keys=[user_id], back_populates="tickets")


class Outbox(Base):
    __tablename__ = "outbox"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type_event = Column(Enum(TypeEvent), nullable=False)
    payload = Column(JSON, nullable=True)
    status = Column(Enum(OutboxStatus), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.now(timezone_msk),
    )


class IdempotencyKeys(Base):
    __table__ = "idempotency_keys"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    request_hash = Column(String)
    ticked_id = Column(String)
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now(timezone_msk),
    )
