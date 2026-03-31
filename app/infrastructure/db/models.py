from datetime import datetime
import uuid
from sqlalchemy import String, Integer, ForeignKey, Column, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
from zoneinfo import ZoneInfo

timezone_msk = ZoneInfo("Europe/Moscow")


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
    status = Column(String, nullable=True)
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
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    last_sync_time = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(timezone_msk),
    )
    last_changed_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(timezone_msk),
    )
    sync_status = Column(String, nullable=False)
