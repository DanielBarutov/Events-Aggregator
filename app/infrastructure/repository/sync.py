from datetime import datetime
import uuid as uuid_lib
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.exceptions import AppError, DatabaseError
from infrastructure.db.models import SyncStatus
from domain.models import SyncStatusEntity

import logging

logger = logging.getLogger(__name__)


class SyncMetadataRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, uuid: str, sync_status: str) -> None:
        try:
            self.session.add(
                SyncStatus(
                    id=uuid,
                    sync_status=sync_status,
                )
            )
            await self.session.commit()
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при создании синхронизации",
                extra={"uuid": uuid},
                details={"reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при создании синхронизации",
                details={"reason": str(e)},
            )

    async def get(self) -> SyncStatusEntity:
        try:
            result = await self.session.execute(
                select(SyncStatus).order_by(SyncStatus.last_sync_time.desc()).limit(1)
            )
            data = result.scalar()
            if not data:
                uuid = str(uuid_lib.uuid4())
                self.session.add(
                    SyncStatus(
                        id=uuid,
                        last_sync_time=datetime(2000, 1, 1, 0, 0, 0),
                        last_changed_at=datetime(2000, 1, 1, 0, 0, 0),
                        sync_status="completed",
                    )
                )
                await self.session.commit()
                return SyncStatusEntity(
                    id=uuid,
                    last_sync_time=datetime(2000, 1, 1, 0, 0, 0),
                    last_changed_at=datetime(2000, 1, 1, 0, 0, 0),
                    sync_status="completed",
                )
            return SyncStatusEntity(
                id=data.id,
                last_sync_time=data.last_sync_time,
                last_changed_at=data.last_changed_at,
                sync_status=data.sync_status,
            )
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении синхронизации",
                extra={"uuid": uuid},
                details={"reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при получении синхронизации",
                details={"reason": str(e)},
            )

    async def update(
        self, uuid: str, sync_status: str, changed_at: datetime = datetime.now()
    ) -> None:
        try:
            result = await self.session.execute(
                select(SyncStatus).where(SyncStatus.id == uuid)
            )
            data = result.scalar()

            data.last_sync_time = datetime.now()
            data.last_changed_at = changed_at
            data.sync_status = sync_status
            await self.session.commit()
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при обновлении синхронизации",
                extra={"uuid": uuid},
                details={"reason": str(e)},
            )
            raise DatabaseError(
                "Неизвестная ошибка при обновлении синхронизации",
                details={"reason": str(e)},
            )
