# Использование as_completed
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
            fetch_status(session, 'https://www.example.com', 1),
            fetch_status(session, 'https://www.example.com', 1),
            fetch_status(session, 'https://www.example.com', 10),
        ]

        for finished_task in asyncio.as_completed(fetchers):
            print(await finished_task)

asyncio.run(main())