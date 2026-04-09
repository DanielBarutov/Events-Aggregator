import logging
from urllib.parse import urljoin

import httpx

from src.domain.exceptions import ExternalProviderError, AppError, InputError
from src.presentation.shemas.event import EventListPydantic
from src.setting import EVENTS_PROVIDER_SERVER, EVENTS_PROVIDER_API_KEY

logger = logging.getLogger(__name__)


class EventsProviderClient:
    def __init__(self):
        self.base_url = EVENTS_PROVIDER_SERVER
        self.headers = {"x-api-key": EVENTS_PROVIDER_API_KEY}
        self.date = "data_from=2000-01-01"

    async def get_events(self, url: str, date: str | None = None) -> EventListPydantic:
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
                return data["seats"]
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
