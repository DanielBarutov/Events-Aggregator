from typing import Any
import logging
import time

from domain.exceptions import AppError, CacheError


logger = logging.getLogger(__name__)


class MemoryCache:
    def __init__(self):
        self._storage: dict[str, tuple[Any, float]] = {}

    def get(self, key: str):
        try:
            item = self._storage.get(key)

            if not item:
                return None

            value, expires_at = item

            if time.time() > expires_at:
                del self._storage[key]
                return None

            return value
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при получении из кэша",
                extra={"key": key, "reason": str(e)},
            )
            raise CacheError(
                "Неизвестная ошибка при получении из кэша", details={"reason": str(e)}
            )

    def set(self, key: str, value: Any, ttl: int):
        try:
            expires_at = time.time() + ttl
            self._storage[key] = (value, expires_at)
        except AppError:
            raise
        except Exception as e:
            logger.exception(
                "Неизвестная ошибка при сохранении в кэш",
                extra={"key": key, "reason": str(e)},
            )
            raise CacheError(
                "Неизвестная ошибка при сохранении в кэш", details={"reason": str(e)}
            )
