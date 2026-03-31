from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
import os
from dotenv import load_dotenv
from domain.exceptions import DatabaseError
import logging

logger = logging.getLogger(__name__)

load_dotenv()

db_url = os.getenv("POSTGRES_CONNECTION_STRING")
if not db_url:
    raise ValueError("POSTGRES_CONNECTION_STRING is not set")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
engine = create_async_engine(db_url)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session():
    try:
        async with AsyncSessionLocal() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
    except Exception as e:
        raise DatabaseError(
            "Неизвестная ошибка при получении сессии", details={"reason": str(e)}
        )
