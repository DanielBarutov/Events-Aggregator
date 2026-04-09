from datetime import date
import logging
from urllib.parse import urljoin

from src.setting import EVENTS_PROVIDER_SERVER
from src.domain.exceptions import AppError, BusinessLogicError, NotFoundError
from src.infrastructure.cache.memory import MemoryCache


logger = logging.getLogger(__name__)
cache = MemoryCache()


class GetEventsUsecase:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.hostname = EVENTS_PROVIDER_SERVER

    async def execute(self, data_from: date, page: int, page_size: int):
        try:
            result = await self.repository.get_events_with_places(data_from)
            sorted_result = sorted(result, key=lambda x: x.event_time, reverse=True)
            return self.get_paginated_result(sorted_result, page, page_size)
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении событий",
                extra={"data_from": data_from},
            )
            raise BusinessLogicError(
                "Неизвестная ошибка при получении событий", details={"reason": str(e)}
            )

    def get_paginated_result(self, result: list, page: int, page_size: int):
        try:
            start = (page - 1) * page_size
            end = start + page_size
            count = len(result)
            next_page = page + 1
            prev_page = page - 1
            data_result = {
                "count": count,
                "next": urljoin(self.hostname, f"/api/events/?page={next_page}")
                if next_page - 2 < (count // page_size)
                else None,
                "previous": urljoin(self.hostname, f"/api/events/?page={prev_page}")
                if prev_page >= 1
                else None,
                "results": result[start:end],
            }
            return data_result
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении событий",
            )
            raise BusinessLogicError(
                "Неизвестная ошибка при получении событий", details={"reason": str(e)}
            )


class GetEventByIdUsecase:
    def __init__(self, repository) -> None:
        self.repository = repository

    async def execute(self, event_id):
        return await self.repository.get_event(event_id)


class GetEventSeatsUsecase:
    def __init__(self, repository, client) -> None:
        self.repository = repository
        self.cache = cache
        self.client = client

    async def execute(self, event_id):
        try:
            memory = cache.get(event_id)
            if memory:
                return memory
            event = await GetEventByIdUsecase(self.repository).execute(event_id)
            if event and event.status == "published":
                available_seats = await self.client.get_available_seats(event_id)
                result = {"event_id": event_id, "available_seats": available_seats}
                cache.set(event_id, result, 60)
            else:
                raise NotFoundError(
                    "Событие не найдено", details={"event_id": event_id}
                )
            return result
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении мест",
                extra={"event_id": event_id},
            )
            raise BusinessLogicError(
                "Неизвестная ошибка при получении мест", details={"reason": str(e)}
            )
