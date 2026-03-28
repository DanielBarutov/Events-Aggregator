from infrastructure.db.session import AsyncSessionLocal
from repository.events import EventsRepository


class GetEventsUsecase:
    def __init__(self):
        self.repository = EventsRepository(AsyncSessionLocal())

    async def execute(self):
        result = await self.repository.get_events_with_places()
        return result
