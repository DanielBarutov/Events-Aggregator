import logging
from urllib.parse import urljoin

import httpx

from src.domain.exceptions import ExternalProviderError, AppError, InputError
from src.infrastructure.clients.dto.events import EventListDTO
from src.infrastructure.clients.cache.memory import MemoryCache

logger = logging.getLogger(__name__)
cache = MemoryCache()


class EventsProviderClient:
    def __init__(self, provider_url, provider_key):
        self.base_url = provider_url
        self.headers = {"x-api-key": provider_key}
        self.date = "data_from=2000-01-01"
        self.cache = cache

    async def get_events(self, url: str, date: str | None = None) -> EventListDTO:
        try:
            if date:
                self.date = f"data_from={date}"
            async with httpx.AsyncClient(base_url=self.base_url, timeout=60) as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                return data
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении событий",
                extra={"url": url, "date": date, "reason": str(e)},
            )
            raise ExternalProviderError(
                "Неизвестная ошибка при получении событий", details={"reason": str(e)}
            )

    async def get_available_seats(self, event_id: str):
        try:
            memory = cache.get(event_id)
            if memory:
                return memory
            async with httpx.AsyncClient() as client:
                url = urljoin(self.base_url, f"/api/events/{event_id}/seats/")
                response = await client.get(url, headers=self.headers)
                if response.status_code == 500:
                    raise InputError(
                        "Ошибка при запросе доступных мест",
                        details={"reason": response.status_code},
                    )
                response.raise_for_status()
                data = response.json()
                cache.set(event_id, data.get("seats"), 60)
                return data.get("seats")
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении доступных мест",
                extra={"event_id": event_id, "reason": str(e)},
            )
            raise ExternalProviderError(
                "Неизвестная ошибка при получении доступных мест",
                details={"reason": str(e)},
            )

    async def create_ticket(
        self, event_id: str, first_name: str, last_name: str, email: str, seat: str
    ):
        try:
            async with httpx.AsyncClient() as client:
                url = urljoin(self.base_url, f"/api/events/{event_id}/register/")
                response = await client.request(
                    method="POST",
                    url=url,
                    headers=self.headers,
                    json={
                        "first_name": first_name,
                        "last_name": last_name,
                        "seat": seat,
                        "email": email,
                    },
                )
                response.raise_for_status()
                return response.json()
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при создании тикета",
                extra={
                    "event_id": event_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "seat": seat,
                    "reason": str(e),
                },
            )
            raise ExternalProviderError(
                "Неизвестная ошибка при создании тикета", details={"reason": str(e)}
            )

    async def delete_ticket(self, event_id: str, ticket_id: str):
        try:
            async with httpx.AsyncClient() as client:
                url = urljoin(self.base_url, f"/api/events/{event_id}/unregister/")
                response = await client.request(
                    method="DELETE",
                    url=url,
                    headers=self.headers,
                    json={"ticket_id": ticket_id},
                )
                response.raise_for_status()
                return response.json()
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при удалении тикета",
                extra={"event_id": event_id, "ticket_id": ticket_id, "reason": str(e)},
            )
            raise ExternalProviderError(
                "Неизвестная ошибка при удалении тикета", details={"reason": str(e)}
            )

    async def iter_events(self, date_from: str):
        paginator = EventsPaginator(self, date_from)
        async for page in paginator:
            yield page


class EventsPaginator:
    def __init__(self, client: EventsProviderClient, date: str | None = None):
        self.client = client
        self.next_page_url = urljoin(
            self.client.base_url, f"/api/events/?data_from={date}"
        )

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.next_page_url is None:
            raise StopAsyncIteration
        data = await self.client.get_events(self.next_page_url)
        self.next_page_url = data.get("next")
        return data.get("results", [])
