import asyncio
from utils import delay


async def main():
    while True:
        delay_time = input('Введите время сна!')
        asyncio.create_task(delay(int(delay_time)))

asyncio.run(main())