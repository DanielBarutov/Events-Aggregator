from sqlalchemy import text

from sqlalchemy.ext.asyncio import AsyncSession


class TestConnectionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def test_connection(self):
        try:
            result = await self.session.execute(text("SELECT 1"))
            return {"status": "ok", "message": "Connection successful", "result": result.scalar()}
        except Exception as e:
            return {"status": "error", "message": "Connection failed", "error": str(e)}
