from datetime import date

from infrastructure.clients.events_provider import EventsProviderClient
from infrastructure.cache.memory import MemoryCache
import os

cache = MemoryCache()


class GetEventsUsecase:
    def __init__(self, repository) -> None:
        self.repository = repository

    async def execute(self, data_from: date, page: int, page_size: int):
        result = await self.repository.get_events_with_places(data_from)
        sorted_result = sorted(result, key=lambda x: x.event_time, reverse=True)
        return self.get_paginated_result(sorted_result, page, page_size)

    def get_paginated_result(self, result: list, page: int, page_size: int):
        start = (page - 1) * page_size
        end = start + page_size
        count = len(result)
        next_page = page + 1
        prev_page = page - 1
        hostname = os.getenv("EVENTS_PROVIDER_SERVER_URL_OUTSIDE")
        data_result = {
            "count": count,
            "next": f"{hostname}/api/events/?page={next_page}"
            if next_page - 2 < (count // page_size)
            else None,
            "previous": f"{hostname}/api/events/?page={prev_page}"
            if prev_page >= 1
            else None,
            "results": result[start:end],
        }
        return data_result


class GetEventByIdUsecase:
    def __init__(self, repository) -> None:
        self.repository = repository

    async def execute(self, event_id):
        return await self.repository.get_event(event_id)


class GetEventSeatsUsecase:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.cache = cache
        self.client = EventsProviderClient()

    async def execute(self, event_id):
        event = await GetEventByIdUsecase(self.repository).execute(event_id)
        if event and event.status == "published":
            available_seats = await self.client.get_available_seats(event_id)
            result = {"event_id": event_id, "available_seats": available_seats}
        else:
            result = {"пока такая 404"}
        return result
