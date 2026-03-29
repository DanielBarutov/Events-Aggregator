import time
from typing import Any


class MemoryCache:
    def __init__(self):
        self._storage: dict[str, tuple[Any, float]] = {}

    def get(self, key: str):
        item = self._storage.get(key)

        if not item:
            return None

        value, expires_at = item

        if time.time() > expires_at:
            del self._storage[key]
            return None

        return value

    def set(self, key: str, value: Any, ttl: int):
        expires_at = time.time() + ttl
        self._storage[key] = (value, expires_at)

    def delete(self, key: str):
        self._storage.pop(key, None)

    def clear(self):
        self._storage.clear()
