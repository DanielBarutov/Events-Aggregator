from datetime import date
from infrastructure.db.session import AsyncSessionLocal
from repository.events import EventsRepository
import os


class GetEventsUsecase:
    def __init__(self):
        self.repository = EventsRepository(AsyncSessionLocal())

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
            "next": f"http://{hostname}/api/events/?page={next_page}"
            if next_page - 2 < (count // page_size)
            else None,
            "previous": f"http://{hostname}/api/events/?page={prev_page}"
            if prev_page >= 1
            else None,
            "results": result[start:end],
        }
        return data_result
