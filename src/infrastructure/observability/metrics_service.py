from src.application.ports.metrics_port import MetricsPort
from src.infrastructure.observability.metrics import (
    TICKETS_CREATED_TOTAL,
    TICKETS_CANCELLED_TOTAL,
)


class PrometheusMetricsService(MetricsPort):
    def inc_tickets_created(self) -> None:
        TICKETS_CREATED_TOTAL.inc()

    def inc_tickets_cancelled(self) -> None:
        TICKETS_CANCELLED_TOTAL.inc()
