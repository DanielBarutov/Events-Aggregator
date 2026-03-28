import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from infrastructure.db.models import Base, Event
from infrastructure.repository.events import EventsRepository


DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await setup_db()

    async with SessionLocal() as session:
        repo = EventsRepository(session)

        # 1. CREATE
        event1 = Event(
            id=1, title="Event 1", changed_at=datetime(2026, 3, 28, 10, 0, 0)
        )
        event2 = Event(
            id=2, title="Event 2", changed_at=datetime(2026, 3, 28, 11, 0, 0)
        )

        await repo.create_events([event1, event2])
        print("CREATE OK")

        # 2. GET
        events = await repo.get_events()
        print("GET EVENTS:", events)

        # 3. LAST CHANGED AT
        last_changed = await repo.get_last_changed_at()
        print("LAST CHANGED AT:", last_changed)

        # 4. UPDATE
        event1.title = "Updated Event 1"
        await repo.update_events([event1])

        updated_events = await repo.get_events()
        print("UPDATED EVENTS:", updated_events)

        # 5. DELETE
        await repo.delete_events([event2])

        remaining = await repo.get_events()
        print("REMAINING EVENTS:", remaining)


if __name__ == "__main__":
    asyncio.run(main())
