import asyncio


async def run_sync_loop(usecase):
    while True:
        await usecase.execute(...)
        await asyncio.sleep(86400)
