from datetime import date
from app.infrastructure.cache.memory import MemoryCache
from utils.generator_seats import GeneratorAvSeats
import os

cache = MemoryCache()


class GetEventsUsecase:
    def __init__(self, repository):
        self.repository = repository

    async def execute(self, data_from: date, page: int, page_size: int):
        result = await self.repository.get_events_with_places()
        sorted_result = sorted(result, key=lambda x: x.event_time)
        if data_from:
            format_result = [
                x for x in sorted_result if x.event_time.date() >= data_from
            ]
            return self.get_paginated_result(format_result, page, page_size)
        else:
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

    async def execute(self, event_id):
        cache_result = self.cache.get("EventSeatsUsecase")
        if cache_result is not None:
            return cache_result
        data_pattern = await self.repository.get_event_seats(event_id)
        data_locked_seats = await self.repository.get_locked_seats(event_id)
        seats_pattern = data_pattern.seats_pattern
        all_seats = GeneratorAvSeats().generate(seats_pattern)
        if data_locked_seats:
            available_seats = GeneratorAvSeats().filter(all_seats, data_locked_seats)
        else:
            available_seats = all_seats
        result = {"event_id": event_id, "available_seats": available_seats}
        self.cache.set("EventSeatsUsecase", result, 30)
        return result
