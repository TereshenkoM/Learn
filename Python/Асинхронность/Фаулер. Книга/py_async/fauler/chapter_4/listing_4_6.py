# Конкурентное выполнение запросов с помощью gather
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
        urls = ['https://www.example.com' for _ in range(1000)]
        # Сгенерировать список сопрограмм для каждого запроса
        requests = [await fetch_status(session, url) for url in urls]
        # Запустить и дождаться выполнения всех запросов
        status_codes = await asyncio.gather(*requests)
        print(status_codes)

asyncio.run(main())

