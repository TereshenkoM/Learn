import asyncio
from chapter_10.listing_10_11 import CircuitBreaker


async def main():
    async def slow_callback():
        await asyncio.sleep(2)

    cb = CircuitBreaker(
        slow_callback,
        timeout=1,
        time_window=5,
        max_failures=2,
        reset_interval=5
    )

    for _ in range(4):
        try:
            await cb.request()
        except Exception as e:
            pass

    print('Засыпаю на 5 с, чтобы прерыватель запустился...')
    await asyncio.sleep(5)

    for _ in range(4):
        try:
            await cb.request()
        except Exception as e:
            pass


asyncio.run(main())