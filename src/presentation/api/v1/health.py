from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/sentry-test")
async def sentry_test():
    raise Exception("Test exception")


@router.get("/sentry-test-2")
async def sentry_test_2():
    return 1 / 0
