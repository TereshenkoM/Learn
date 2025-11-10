# Обработка исключений в asyncio.gather
import asyncio
import aiohttp
from aiohttp import ClientSession
from utils import async_timed


async def fetch_status(session: ClientSession, url: str) -> int:
    async with session.get(url) as result:
        return result.status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://www.example.com', 'python://ru']
        requests = [fetch_status(session, url) for url in urls]
        # По дефолту False. Возбудит исключение, но другие задачи продолжат работу (в случае, если исключение обработается)
        # status_codes = await asyncio.gather(*requests, return_exceptions=False)

        # Не возбудит исключение, а просто вернёт его
        results = await asyncio.gather(*requests, return_exceptions=True)

        print('Ошибки', [res for res in results if isinstance(res, Exception)])
        print('Успех', [res for res in results if not isinstance(res, Exception)])

asyncio.run(main())

