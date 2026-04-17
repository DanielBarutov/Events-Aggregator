from prometheus_client import Counter, Histogram, Gauge

# HTTP
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

# EventProvider
EVENTS_PROVIDER_REQUESTS_TOTAL = Counter(
    "events_provider_requests_total",
    "Total requests to Events Provider API",
    ["endpoint", "status"],
)

EVENTS_PROVIDER_REQUEST_DURATION_SECONDS = Histogram(
    "events_provider_request_duration_seconds",
    "Events Provider API request duration in seconds",
    ["endpoint"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

# Usecases
TICKETS_CREATED_TOTAL = Counter(
    "tickets_created_total",
    "Total created tickets",
)

TICKETS_CANCELLED_TOTAL = Counter(
    "tickets_cancelled_total",
    "Total cancelled tickets",
)

EVENTS_TOTAL = Gauge(
    "events_total",
    "Current number of events in database",
)

# Cache
CACHE_HITS_TOTAL = Counter(
    "cache_hits_total",
    "Cache hits for seats",
)

CACHE_MISSES_TOTAL = Counter(
    "cache_misses_total",
    "Cache misses for seats",
)
