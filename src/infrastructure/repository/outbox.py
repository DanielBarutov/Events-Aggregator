from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.models import Outbox, OutboxStatus
from src.domain.models import OutboxEntity
from src.domain.exceptions import NotFoundError


class OutboxRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_outbox(self) -> list[OutboxEntity] | None:
        try:
            data = await self.session.execute(
                select(Outbox).where(OutboxStatus == "await")
            )
            outboxes = data.scalars().all()
            return (
                [
                    OutboxEntity(
                        id=outbox.id,
                        type_event=outbox.type_event,
                        payload=outbox.payload,
                        status=outbox.status,
                        retry=outbox.retry,
                        created_at=outbox.created_at,
                    )
                    for outbox in outboxes
                ]
                if outboxes
                else None
            )
        except Exception as e:
            raise e

    async def add_retry(self, outbox_id: str) -> None:
        try:
            data = await self.session.execute(
                select(Outbox).where(Outbox.id == outbox_id)
            )
            outbox: Outbox = data.scalar()
            if not outbox:
                raise NotFoundError(
                    "При смене статуса у outbox, не был найден outbox в БД"
                )
            outbox.retry += 1
            await self.session.commit()
            await self.session.refresh(outbox)
        except Exception as e:
            raise e

    async def change_outbox_status(self, outbox_id: str, status: str) -> None:
        try:
            data = await self.session.execute(
                select(Outbox).where(Outbox.id == outbox_id)
            )
            outbox: Outbox = data.scalar()
            if not outbox:
                raise NotFoundError(
                    "При смене статуса у outbox, не был найден outbox в БД"
                )
            if status == "sent":
                outbox.status = OutboxStatus.sent
            if status == "fail":
                outbox.status = OutboxStatus.fail
            await self.session.commit()
            await self.session.refresh(outbox)
        except Exception as e:
            await self.session.rollback()
            raise e
