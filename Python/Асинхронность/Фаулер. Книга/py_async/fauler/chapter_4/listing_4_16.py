# Использование тайм-аутов в wait
import asyncio
import aiohttp
from utils import async_timed
from aiohttp import ClientSession


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
        url = 'https://example.com'

        api_a = fetch_status(session, url)
        api_b = fetch_status(session, url)


        done, pending = await asyncio.wait([api_a, api_b], timeout=1)

        for task in pending:
            if task is api_b:
                print('API B слишком медленный, отмена')
                task.cancel()

asyncio.run(main())