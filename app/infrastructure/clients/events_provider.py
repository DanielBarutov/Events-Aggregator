import httpx

from app.shemas.event import EventListPydantic


class EventsProviderClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"x-api-key": api_key}

    async def get_by_url(self, url: str) -> EventListPydantic:
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if data["next"]:
                data["next"] = data["next"].replace("http", "https")
            if data["previous"]:
                data["previous"] = data["previous"].replace("http", "https")
            return data
