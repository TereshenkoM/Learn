import aiohttp
from aiohttp import ClientSession
import asyncio
import logging
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
            asyncio.create_task(fetch_status(session, 'python://bad/com')),
            asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=3)),
            asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=3))
        ]

        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_EXCEPTION)

        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error('При выполнении запроса возникло исключение', exc_info=done_task.exception())
        
        for pending_task in pending:
            pending_task.cancel()

asyncio.run(main())