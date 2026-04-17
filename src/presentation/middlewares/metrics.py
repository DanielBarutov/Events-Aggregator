import time
from fastapi import Request
from starlette.responses import Response

from src.infrastructure.observability.metrics import (
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_DURATION_SECONDS,
)


async def metrics_middleware(request: Request, call_next) -> Response:
    start = time.perf_counter()
    method = request.method

    endpoint = request.url.path

    try:
        response = await call_next(request)
        status = str(response.status_code)
        return response
    except Exception:
        status = "500"
        raise
    finally:
        route = request.scope.get("route")
        if route and hasattr(route, "path"):
            endpoint = route.path

        duration = time.perf_counter() - start
        HTTP_REQUESTS_TOTAL.labels(
            method=method,
            endpoint=endpoint,
            status=status,
        ).inc()
        HTTP_REQUEST_DURATION_SECONDS.labels(
            method=method,
            endpoint=endpoint,
        ).observe(duration)
