# Изучение поведения wait по умолчанию
import asyncio
import aiohttp
from aiohttp import ClientSession
from utils import async_timed


async def fetch_status(
    session: ClientSession,
    url: str,
    delay: int = 0
) -> int:
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'https://example.com', 1)),
            asyncio.create_task(fetch_status(session, 'https://example.com', 1))
        ]
        done, pending = await asyncio.wait(fetchers)

        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')

        for done_task in done:
            result = await done_task
            print(result)

asyncio.run(main())